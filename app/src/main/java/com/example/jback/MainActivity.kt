// This file was moved to `app/src/main/java/com/jback/rootbackup/MainActivity.kt`
// Original content preserved in the new location. Keep this placeholder to avoid accidental use.

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
        
        // Extract to temp file first
        val tempFile = File.createTempFile("restore", ".tmp", cacheDir)
        tempFile.outputStream().use { zis.copyTo(it) }
        
        // Copy to destination using root
        Shell.cmd("cp \"${tempFile.absolutePath}\" \"$targetPath\"").exec()
        tempFile.delete()
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
