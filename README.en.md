# RE-Maya-Animation-Export-Tool

[English](./README.en.md) | [中文](./README.md)

Based on the MaxScript from fmt_RE_MESH-Noesis-Plugin, this project provides a Maya version with the following features:

* Open and import .mesh and .motlist files directly in Maya
* Batch animation splitting
* Fix for the issue where animations exported with Noesis default to 30fps, causing them to appear at half speed

## REEM Plugin Setup

* Open Maya, **go to Windows → General Editors → Script Editor**.
* In the Script Editor, go to **File → Open Script**, and load the downloaded **RE Engine Mesh/Animation Noesis Tool** script.
* In the Script Editor, go to **File → Save Script to Shelf** to add it as a Maya shelf tool.

Once the REEM plugin is open, you can either use **Browse** to locate Noesis or enter its path directly.

## Exporting Animations from `.motlist`

* Click the **Import Mesh/Animation** button in REEM.
* Select the `.motlist.XXXXXXXXXX` file you want to unpack.
* An animation selection panel will appear:
  * Double-click the first entry starting with `[ALL]` to add it to Motions to load.
  * Double-clicking again in the list will deselect it.

The `fmt_RE_MESH-Noesis-Plugin` generates a single `[ALL]` animation sequence containing all animations in a `.motlist`.

Click `Load` to export. Once complete, all animations will be imported into the Maya scene.

## Splitting Animations in Maya

After import, the **Animation List** will be automatically filled using the log output from `fmt_RE_MESH-Noesis-Plugin`.

* Switching between entries will update the timeline to the corresponding animation range.

In **Export Options**:

* **Export Selected Animations**: Export only the selected animation clips.
* **Export All Animations**: Export all clips from the list.

To export, select the animation skeleton in the scene, click **Export**, and choose a save path.

## Important Notes

The `fmt_RE_MESH-Noesis-Plugin` may fail to parse certain animations from a `.motlist`.
In these cases, it may output only the first frame but still log the full frame count.
This can cause mismatches between the Animation List and the actual imported animations.

Fixes implemented:
* If the log reports a **Warning** that an animation cannot be exported, that animation is removed from the **Animation List**.
* If the log reports **0 frames**, it will be set to **1 frame**.
* If the animation name contains **blend_pose**, it will be set to **1 frame**.

Despite these fixes, some animations may still export with only 1 frame without errors.

Manual Fix:

1. Open Maya’s Script Editor and check the log panel for the export log.
2. Copy the log text and change the `frames` value of problematic entries to **1**.
3. Click the **Manually Paste Noesis List** button, paste the modified log, and the **Animation List** will be corrected.
4. Re-select the corrected entries in the Animation List to confirm they are marked as **1 frame**.

⚠️ Note: Animations with this issue may cause errors when imported into **Unreal Engine 5.6**.
