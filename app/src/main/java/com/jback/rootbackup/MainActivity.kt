package com.jback.rootbackup

import android.Manifest
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.Settings
import android.widget.*
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.view.isVisible
import com.topjohnwu.superuser.Shell
import kotlinx.coroutines.*
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import com.topjohnwu.superuser.io.SuFile
import com.topjohnwu.superuser.io.SuFileInputStream
import com.topjohnwu.superuser.io.SuFileOutputStream
import java.text.SimpleDateFormat
import java.util.*
import java.util.zip.ZipEntry
import java.util.zip.ZipInputStream
import java.util.zip.ZipOutputStream

class MainActivity : AppCompatActivity() {

    companion object {
        private const val REQUEST_PERMS = 1001
    }

    private lateinit var btnCheckRoot: Button
    private lateinit var btnSelectAll: Button
    private lateinit var btnBackup: Button
    private lateinit var btnRestore: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var txtStatus: TextView
    private lateinit var listViewApps: ListView
    private lateinit var switchBackupData: Switch
    private lateinit var switchBackupFolders: Switch

    private val appList = mutableListOf<AppInfo>()
    private val selectedApps = mutableSetOf<String>()
    private var isRootAvailable = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initializeViews()
        setupClickListeners()
        checkRootAccess()
        loadInstalledApps()
    }

    private fun initializeViews() {
        btnCheckRoot = findViewById(R.id.btnCheckRoot)
        btnSelectAll = findViewById(R.id.btnSelectAll)
        btnBackup = findViewById(R.id.btnBackup)
        btnRestore = findViewById(R.id.btnRestore)
        progressBar = findViewById(R.id.progressBar)
        txtStatus = findViewById(R.id.txtStatus)
        listViewApps = findViewById(R.id.listViewApps)
        switchBackupData = findViewById(R.id.switchBackupData)
        switchBackupFolders = findViewById(R.id.switchBackupFolders)
    }

    private fun setupClickListeners() {
        btnCheckRoot.setOnClickListener { checkRootAccess() }
        btnSelectAll.setOnClickListener { selectAllApps() }
        btnBackup.setOnClickListener { startBackup() }
        btnRestore.setOnClickListener { showRestoreDialog() }

        listViewApps.setOnItemClickListener { _, _, position, _ ->
            val app = appList[position]
            if (selectedApps.contains(app.packageName)) {
                selectedApps.remove(app.packageName)
            } else {
                selectedApps.add(app.packageName)
            }
            updateAppList()
        }
    }

    private fun checkRootAccess() {
        txtStatus.text = "Checking root access..."
        CoroutineScope(Dispatchers.Main).launch {
            withContext(Dispatchers.IO) {
                isRootAvailable = Shell.isAppGrantedRoot() == true
            }
            if (isRootAvailable) {
                txtStatus.text = "✓ Root access granted"
                btnBackup.isEnabled = true
                btnRestore.isEnabled = true
            } else {
                txtStatus.text = "✗ Root access denied"
                btnBackup.isEnabled = false
                btnRestore.isEnabled = false
                Toast.makeText(
                    this@MainActivity,
                    "Root access is required for this app",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }

    private fun loadInstalledApps() {
        CoroutineScope(Dispatchers.Main).launch {
            withContext(Dispatchers.IO) {
                val packages = packageManager.getInstalledPackages(0)
                appList.clear()
                packages.forEach { pkg ->
                    val appInfo = AppInfo(
                        packageName = pkg.packageName,
                        name = pkg.applicationInfo.loadLabel(packageManager).toString(),
                        icon = pkg.applicationInfo.loadIcon(packageManager),
                        sourceDir = pkg.applicationInfo.sourceDir
                    )
                    appList.add(appInfo)
                }
                appList.sortBy { it.name.toLowerCase(Locale.getDefault()) }
            }
            updateAppList()
        }
    }

    private fun updateAppList() {
        val adapter = ArrayAdapter(
            this, android.R.layout.simple_list_item_multiple_choice,
            appList.map {
                "${it.name}\n${it.packageName}" +
                        if (selectedApps.contains(it.packageName)) " ✓" else ""
            }
        )
        listViewApps.adapter = adapter

        for (i in 0 until appList.size) {
            listViewApps.setItemChecked(i, selectedApps.contains(appList[i].packageName))
        }
    }

    private fun selectAllApps() {
        if (selectedApps.size == appList.size) {
            selectedApps.clear()
        } else {
            selectedApps.clear()
            appList.forEach { selectedApps.add(it.packageName) }
        }
        updateAppList()
    }

    private fun startBackup() {
        if (!isRootAvailable) {
            Toast.makeText(this, "Root access required", Toast.LENGTH_SHORT).show()
            return
        }

        if (!ensureStoragePermissions()) return

        if (selectedApps.isEmpty() && !switchBackupFolders.isChecked) {
            Toast.makeText(this, "Select apps or folders to backup", Toast.LENGTH_SHORT).show()
            return
        }

        CoroutineScope(Dispatchers.Main).launch {
            progressBar.isVisible = true
            btnBackup.isEnabled = false

            val result = withContext(Dispatchers.IO) {
                performBackup()
            }

            progressBar.isVisible = false
            btnBackup.isEnabled = true

            if (result.isSuccess) {
                txtStatus.text = "Backup completed: ${result.getOrNull()}"
                Toast.makeText(this@MainActivity, "Backup successful!", Toast.LENGTH_LONG).show()
            } else {
                txtStatus.text = "Backup failed: ${result.exceptionOrNull()?.message}"
                Toast.makeText(this@MainActivity, "Backup failed!", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun ensureStoragePermissions(): Boolean {
        // For Android 11+ require MANAGE_EXTERNAL_STORAGE
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                AlertDialog.Builder(this)
                    .setTitle("Permission required")
                    .setMessage("Grant All Files Access so the app can read/write backups. You'll be taken to Settings to enable it.")
                    .setPositiveButton("Open Settings") { _, _ ->
                        val intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                        val uri: Uri = Uri.fromParts("package", packageName, null)
                        intent.data = uri
                        startActivity(intent)
                    }
                    .setNegativeButton("Cancel", null)
                    .show()
                return false
            }
        } else {
            // Request runtime read/write permissions for older Android versions
            val permsNeeded = mutableListOf<String>()
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                permsNeeded.add(Manifest.permission.READ_EXTERNAL_STORAGE)
            }
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                permsNeeded.add(Manifest.permission.WRITE_EXTERNAL_STORAGE)
            }
            if (permsNeeded.isNotEmpty()) {
                ActivityCompat.requestPermissions(this, permsNeeded.toTypedArray(), REQUEST_PERMS)
                return false
            }
        }
        return true
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_PERMS) {
            // Re-check permissions and notify user
            Toast.makeText(this, "Permissions updated. Please retry the operation.", Toast.LENGTH_SHORT).show()
        }
    }

    private fun performBackup(): Result<String> {
        return try {
            val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
            val backupDir = File(getExternalFilesDir(null), "Backups")
            if (!backupDir.exists()) backupDir.mkdirs()

            val backupFile = File(backupDir, "full_backup_$timestamp.zip")

            FileOutputStream(backupFile).use { fos ->
                ZipOutputStream(fos).use { zos ->
                    // Backup selected apps
                    if (selectedApps.isNotEmpty()) {
                        backupAppsToZip(zos)
                    }

                    // Backup folders
                    if (switchBackupFolders.isChecked) {
                        backupFoldersToZip(zos)
                    }

                    // Create backup manifest
                    createManifest(zos)
                }
            }

            Result.success(backupFile.absolutePath)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun backupAppsToZip(zos: ZipOutputStream) {
        selectedApps.forEach { packageName ->
            val appInfo = appList.find { it.packageName == packageName } ?: return@forEach

            // Backup APK
            backupApk(appInfo, zos)

            // Backup app data if enabled
            if (switchBackupData.isChecked) {
                backupAppData(appInfo, zos)
            }
        }
    }

    private fun backupApk(appInfo: AppInfo, zos: ZipOutputStream) {
        try {
            val apkFile = File(appInfo.sourceDir)
            if (apkFile.exists()) {
                val zipEntry = ZipEntry("apps/${appInfo.packageName}.apk")
                zos.putNextEntry(zipEntry)
                apkFile.inputStream().use { it.copyTo(zos) }
                zos.closeEntry()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun backupAppData(appInfo: AppInfo, zos: ZipOutputStream) {
        try {
            // Backup /data/data/package
            val dataPath = "/data/data/${appInfo.packageName}"
            val dataSu = SuFile(dataPath)
            if (dataSu.exists()) {
                addFolderToZipSu(dataSu, "app_data/${appInfo.packageName}", zos)
            }

            // Backup external data if exists
            val externalDir = File("/sdcard/Android/data/${appInfo.packageName}")
            if (externalDir.exists()) {
                addFolderToZip(externalDir, "external_data/${appInfo.packageName}", zos)
            }

            // Backup obb data if exists
            val obbDir = File("/sdcard/Android/obb/${appInfo.packageName}")
            if (obbDir.exists()) {
                addFolderToZip(obbDir, "obb_data/${appInfo.packageName}", zos)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun backupFoldersToZip(zos: ZipOutputStream) {
        val foldersToBackup = listOf(
            "/sdcard/DCIM",
            "/sdcard/Documents",
            "/sdcard/Download",
            "/sdcard/Downloads",
            "/sdcard/Movies",
            "/sdcard/Music",
            "/sdcard/Pictures",
            "/sdcard/Telegram",
            "/sdcard/WhatsApp",
            "/sdcard/Signal",
            "/sdcard/Messenger",
            "/sdcard/Videos"
        )

        foldersToBackup.forEach { folderPath ->
            val folder = File(folderPath)
            if (folder.exists() && folder.isDirectory) {
                try {
                    addFolderToZip(folder, "user_data/${folder.name}", zos)
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    }

    private fun addFolderToZip(folder: File, basePath: String, zos: ZipOutputStream) {
        folder.walk().forEach { file ->
            if (file.isFile) {
                try {
                    val relativePath = basePath + folder.toURI().relativize(file.toURI()).path
                    val zipEntry = ZipEntry(relativePath)
                    zos.putNextEntry(zipEntry)
                    file.inputStream().use { it.copyTo(zos) }
                    zos.closeEntry()
                } catch (e: Exception) {
                    // Continue with next file
                }
            }
        }
    }

    private fun addFolderToZipSu(folder: SuFile, basePath: String, zos: ZipOutputStream) {
        try {
            val files = folder.listFiles() ?: return
            files.forEach { f ->
                if (f.isDirectory) {
                    addFolderToZipSu(f, basePath + f.name + "/", zos)
                } else if (f.isFile) {
                    try {
                        val relativePath = basePath + folder.toURI().relativize(File(f.canonicalPath).toURI()).path
                        val zipEntry = ZipEntry(relativePath)
                        zos.putNextEntry(zipEntry)
                        SuFileInputStream(f).use { it.copyTo(zos) }
                        zos.closeEntry()
                    } catch (e: Exception) {
                        // continue
                    }
                }
            }
        } catch (e: Exception) {
            // best-effort
        }
    }

    private fun createManifest(zos: ZipOutputStream) {
        try {
            val manifest = """
            |Backup created: ${Date()}
            |Apps backed up: ${selectedApps.size}
            |App data: ${switchBackupData.isChecked}
            |Folders: ${switchBackupFolders.isChecked}
            |Root access: $isRootAvailable
            """.trimMargin()

            val zipEntry = ZipEntry("backup_manifest.txt")
            zos.putNextEntry(zipEntry)
            zos.write(manifest.toByteArray())
            zos.closeEntry()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun showRestoreDialog() {
        val backupDir = File(getExternalFilesDir(null), "Backups")
        if (!backupDir.exists() || backupDir.listFiles()?.isEmpty() != false) {
            Toast.makeText(this, "No backups found", Toast.LENGTH_SHORT).show()
            return
        }

        val backups = backupDir.listFiles { file -> file.name.endsWith(".zip") }?.toList() ?: emptyList()

        val backupNames = backups.map { it.name }.toTypedArray()

        AlertDialog.Builder(this)
            .setTitle("Select Backup to Restore")
            .setItems(backupNames) { _, which ->
                val selectedBackup = backups[which]
                confirmRestore(selectedBackup)
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun confirmRestore(backupFile: File) {
        AlertDialog.Builder(this)
            .setTitle("Confirm Restore")
            .setMessage("Restore from ${backupFile.name}? This will overwrite existing data!")
            .setPositiveButton("Restore") { _, _ ->
                startRestore(backupFile)
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun startRestore(backupFile: File) {
        if (!ensureStoragePermissions()) return

        CoroutineScope(Dispatchers.Main).launch {
            progressBar.isVisible = true
            btnRestore.isEnabled = false

            val result = withContext(Dispatchers.IO) {
                performRestore(backupFile)
            }

            progressBar.isVisible = false
            btnRestore.isEnabled = true

            if (result.isSuccess) {
                txtStatus.text = "Restore completed successfully"
                Toast.makeText(this@MainActivity, "Restore successful!", Toast.LENGTH_LONG).show()
            } else {
                txtStatus.text = "Restore failed: ${result.exceptionOrNull()?.message}"
                Toast.makeText(this@MainActivity, "Restore failed!", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun performRestore(backupFile: File): Result<Unit> {
        return try {
            FileInputStream(backupFile).use { fis ->
                ZipInputStream(fis).use { zis ->
                    var entry: ZipEntry?
                    // Track packages whose data we restored so we can fix ownership/SELinux afterwards
                    val restoredPackages = mutableSetOf<String>()
                    while (zis.nextEntry.also { entry = it } != null) {
                        val entryName = entry!!.name

                        when {
                            entryName.startsWith("apps/") && entryName.endsWith(".apk") -> {
                                restoreApk(zis, entryName)
                            }
                            entryName.startsWith("app_data/") -> {
                                val pkg = entryName.removePrefix("app_data/").split('/')[0]
                                restoreAppData(zis, entryName)
                                restoredPackages.add(pkg)
                            }
                            entryName.startsWith("user_data/") -> {
                                restoreUserData(zis, entryName)
                            }
                        }
                        zis.closeEntry()
                    }

                    // After extracting, fix ownership and SELinux context for restored app data
                    restoredPackages.forEach { pkg ->
                        try {
                            val uid = try {
                                packageManager.getPackageInfo(pkg, 0).applicationInfo.uid
                            } catch (e: Exception) {
                                -1
                            }
                            if (uid != -1) {
                                // chown -R uid:uid /data/data/<pkg>
                                Shell.cmd("chown -R $uid:$uid /data/data/$pkg").exec()
                                // fix permissions (best-effort)
                                Shell.cmd("chmod -R 700 /data/data/$pkg").exec()
                                // restore SELinux context
                                Shell.cmd("restorecon -R /data/data/$pkg").exec()
                            }
                        } catch (e: Exception) {
                            // continue with next package
                        }
                    }
                }
            }
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun restoreApk(zis: ZipInputStream, entryName: String) {
        // Extract APK to temp location
        val tempDir = File(cacheDir, "apk_restore")
        if (!tempDir.exists()) tempDir.mkdirs()

        val apkFile = File(tempDir, entryName.substringAfterLast("/"))
        apkFile.outputStream().use { zis.copyTo(it) }

        // Install APK using root
        Shell.cmd("pm install -r \"${apkFile.absolutePath}\"").exec()
    }

    private fun restoreAppData(zis: ZipInputStream, entryName: String) {
        val relativePath = entryName.substringAfter("app_data/")
        val targetPath = "/data/data/$relativePath"
        
        // Write directly to protected destination using libsu SuFileOutputStream
        try {
            val targetSu = SuFile(targetPath)
            // Ensure parent exists
            targetSu.parentFile?.let { p -> if (!p.exists()) p.mkdirs() }
            SuFileOutputStream(targetSu).use { out ->
                zis.copyTo(out)
            }
        } catch (e: Exception) {
            // Fallback: extract to temp and copy via shell
            val tempFile = File.createTempFile("restore", ".tmp", cacheDir)
            tempFile.outputStream().use { zis.copyTo(it) }
            Shell.cmd("cp \"${tempFile.absolutePath}\" \"$targetPath\"").exec()
            tempFile.delete()
        }
    }

    private fun restoreUserData(zis: ZipInputStream, entryName: String) {
        val relativePath = entryName.substringAfter("user_data/")
        val targetPath = "/sdcard/$relativePath"

        // Create parent directory
        val targetFile = File(targetPath)
        targetFile.parentFile?.mkdirs()

        targetFile.outputStream().use { zis.copyTo(it) }
    }
}

data class AppInfo(
    val packageName: String,
    val name: String,
    val icon: android.graphics.drawable.Drawable,
    val sourceDir: String
)
