import importlib.util
import os
import pathlib
import subprocess
import sys
import types
import unittest
from unittest import mock


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "REEM_Noesis_Maya.py"


def load_script_module():
    maya_module = types.ModuleType("maya")
    maya_cmds_module = types.ModuleType("maya.cmds")
    maya_mel_module = types.ModuleType("maya.mel")
    maya_module.cmds = maya_cmds_module
    maya_module.mel = maya_mel_module

    sys.modules["maya"] = maya_module
    sys.modules["maya.cmds"] = maya_cmds_module
    sys.modules["maya.mel"] = maya_mel_module

    spec = importlib.util.spec_from_file_location("reem_noesis_maya", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NoesisLauncherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_script_module()

    def test_build_command_can_enable_non_interactive_plugin_loading(self):
        command = self.module.build_noesis_command(
            noesis_path=r"F:\Tools Folder\Noesis64.exe",
            input_file=r"F:\Game Assets\sample.mesh.231011879",
            fbx_path=r"F:\Game Assets\sample.fbx",
            log_path=r"F:\Game Assets\sample_noesis.txt",
            optimize=False,
            framerate=60,
            batch=True,
            no_prompt=True,
        )

        self.assertIn(r'"F:\Tools Folder\Noesis64.exe" ?cmode', command)
        self.assertIn("-fbxnooptimize", command)
        self.assertIn("-fbxmeshmerge", command)
        self.assertIn("-logfile", command)
        self.assertIn("-fbxframerate 60", command)
        self.assertIn("-b", command)
        self.assertIn("-noprompt", command)

    def test_build_command_keeps_plugin_selection_dialogs_by_default(self):
        command = self.module.build_noesis_command(
            noesis_path=r"F:\Noesis\Noesis64.exe",
            input_file=r"F:\Game\sample.motlist.751",
            fbx_path=r"F:\Game\sample.fbx",
            log_path=r"F:\Game\sample_noesis.txt",
        )

        self.assertNotIn(" -b", command)
        self.assertNotIn("-noprompt", command)

    @mock.patch("subprocess.Popen")
    def test_launcher_uses_hidden_cp936_console_without_redirected_pipes(self, popen):
        process = mock.Mock()
        popen.return_value = process

        returned = self.module.launch_noesis_command(
            '"F:\\Noesis\\Noesis64.exe" ?cmode "input.mesh" "output.fbx"',
            r"F:\Noesis",
        )

        self.assertIs(returned, process)
        args, kwargs = popen.call_args
        self.assertTrue(args[0].startswith("chcp 936>nul & "))
        self.assertTrue(kwargs["shell"])
        self.assertEqual(kwargs["cwd"], r"F:\Noesis")
        self.assertEqual(kwargs["creationflags"], subprocess.CREATE_NEW_CONSOLE)
        self.assertEqual(kwargs["startupinfo"].wShowWindow, subprocess.SW_HIDE)
        self.assertNotIn("stdout", kwargs)
        self.assertNotIn("stderr", kwargs)

    @unittest.skipUnless(
        os.environ.get("REEM_RUN_NOESIS_INTEGRATION") == "1",
        "set REEM_RUN_NOESIS_INTEGRATION=1 to run the real Noesis export",
    )
    def test_real_noesis_export_creates_binary_fbx(self):
        noesis_path = os.environ["REEM_NOESIS_PATH"]
        input_file = os.environ["REEM_SAMPLE_PATH"]
        output_directory = pathlib.Path(os.environ["REEM_OUTPUT_DIR"])
        output_directory.mkdir(parents=True, exist_ok=True)

        fbx_path = output_directory / "out.fbx"
        log_path = output_directory / "noesis.txt"
        command = self.module.build_noesis_command(
            noesis_path=noesis_path,
            input_file=input_file,
            fbx_path=str(fbx_path),
            log_path=str(log_path),
            batch=True,
            no_prompt=True,
        )

        process = self.module.launch_noesis_command(
            command,
            str(pathlib.Path(noesis_path).parent),
        )
        return_code = process.wait(timeout=120)

        self.assertEqual(return_code, 0)
        self.assertTrue(fbx_path.is_file())
        self.assertGreater(fbx_path.stat().st_size, 1024)
        self.assertEqual(fbx_path.read_bytes()[:18], b"Kaydara FBX Binary")


if __name__ == "__main__":
    unittest.main()
