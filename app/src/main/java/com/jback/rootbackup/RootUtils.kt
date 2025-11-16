package com.jback.rootbackup

import com.topjohnwu.superuser.Shell

object RootUtils {
    fun execRootCommand(cmd: String, timeoutMs: Long = 30_000): String? {
        return try {
            // Use libsu Shell API which handles root interactions reliably
            val result = Shell.cmd(cmd).exec() // returns a List<String> of output lines
            if (result.isNotEmpty()) result.joinToString("\n") else ""
        } catch (e: Exception) {
            // Fallback to Runtime.exec if libsu isn't available (best-effort)
            try {
                val p = Runtime.getRuntime().exec(arrayOf("su", "-c", cmd))
                val out = p.inputStream.bufferedReader().use { it.readText() }
                p.waitFor()
                out
            } catch (ex: Exception) {
                ex.stackTraceToString()
            }
        }
    }

    fun isDeviceRooted(): Boolean {
        return try {
            Shell.isAppGrantedRoot() == true
        } catch (e: Exception) {
            // Fallback check
            try {
                val p = Runtime.getRuntime().exec(arrayOf("su", "-c", "id"))
                p.waitFor()
                p.exitValue() == 0
            } catch (ex: Exception) {
                false
            }
        }
    }
}

