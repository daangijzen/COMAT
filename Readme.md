# **Copilot's Mixamo Animation Transfer (COMAT)**  
### 📌 Automate Mixamo Animation Retargeting in Blender  

**COMAT** simplifies the process of transferring Mixamo animations to any custom rig in Blender, avoiding tedious manual rework.  

## 🚀 Features  
✅ **Easy UI Integration** – Located in Blender’s **N-panel** under `COMAT`.  
✅ **Browse for FBX Files** – Select Mixamo animations directly.  
✅ **Automatic Action Transfer** – Saves animations as new actions instead of overwriting.  
✅ **Undo Functionality** – Revert the last animation transfer if needed.  
✅ **Future Plans** – Batch processing for multiple animations at once.  

## 🛠 Installation Guide  
1. **Download COMAT** (`COMAT.zip`).  
2. In Blender, navigate to **Edit → Preferences → Add-ons → Install**.  
3. Select `COMAT.zip` and click **Install Add-on from File**.  
4. Enable `Copilot's Mixamo Animation Transfer (COMAT)`.  
5. Open the **N-panel** (`View → Sidebar → COMAT`).  

## 🎬 How to Retarget Mixamo Animations  
### Step-by-Step Guide  

1️⃣ **Import Your Character Rig**  
- Ensure your custom skeleton is set up properly in Blender.  
- Place it in **T-Pose** for optimal retargeting.  

2️⃣ **Select Your Target Armature**  
- Click your **custom rig** in the **3D Viewport** to mark it as the animation target.  

3️⃣ **Open COMAT and Select Animation**  
- Go to the **COMAT tab** in the N-panel.  
- Click **Browse**, select your **Mixamo FBX animation**, and confirm.  

4️⃣ **Transfer Animation**  
- Click **Transfer Animation to Selected**.  
- The animation will be applied as a new action.  

5️⃣ **Refine the Animation (Optional)**  
- Adjust **Bone Constraints** or tweak animations in the **Graph Editor**.  
- Use Blender’s **Retargeting Tools** (such as Rokoko or Auto-Rig Pro) for advanced corrections.  

6️⃣ **Undo If Needed**  
- If the animation doesn’t align properly, simply hit **Undo Last Transfer** to revert.  

## 🔥 Roadmap  
🔹 **Batch Animation Processing** – Apply multiple animations in one click.  
🔹 **Advanced Bone Remapping** – Fine-tune Mixamo skeleton compatibility.  
🔹 **Pose Correction Tool** – Auto-adjust Mixamo’s T-pose to fit different rigs.


## Copyright
I basically vibecoded this thing together with the use of copilot, so there's really no copyright. Do with this as you please!