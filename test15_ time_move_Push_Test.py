from omni.isaac.kit import SimulationApp
CONFIG = {
    "headless": False,
    "width": 1920,
    "height": 1080,
    "renderer": "None",
}
simulation_app = SimulationApp(CONFIG)

from isaacsim.core.api import World
import numpy as np
import omni.ui as ui
from omni.isaac.core.utils.stage import add_reference_to_stage
from isaacsim.core.api.robots import Robot
from isaacsim.storage.native import get_assets_root_path
from omni.usd import get_context
import time  # ← 請放在程式最上方

# 新增牆上時間用變數
wall_start_time = None

context = get_context()
usd_path = r"C:\\Users\\admin\\Desktop\\Omniverse\\Isaac Sim\\UR20_RealMotion_4_3_2.usd"
context.open_stage(usd_path)
print("✅ 已成功打開:", usd_path)

world = World()
world.reset()
stage = context.get_stage()
ur20 = world.scene.add(Robot(prim_path="/World/ur20", name="ur20"))

# 6. 準備關節目標
target_joint_positions_rad = [
    np.deg2rad([-6.5, -86.5, 95.1, -108.5, -88.5, -28.3]), #起始點
    np.deg2rad([39, -46.9, 82.1, -34.5, -46.9, -44.7]),#1  新工具調整若OK 會寫OK
    np.deg2rad([45.7, -50, 80.6, -30, -44.7, -44.7]),#2 OK
    np.deg2rad([51, -73.9, 91.3, -97.8, -96.5, -85.8]),#3 OK
    np.deg2rad([62.9, -68.6, 95.9, -115.1, -91.2, -77.9]),#4 OK
    np.deg2rad([-16.8, -39.3, 44.8, -93.8, -89.8, 29.7]),#5 OK
    np.deg2rad([-28.7, -52.6, 73.3, -111.1, -89.8, 17.8]),#6 OK
    np.deg2rad([13.8, -84.5, 119.8, -124.4, -88.5, 57.6]),#7 OK
    np.deg2rad([4.1, -50.7, 85.4, -36, -83, -43.8]),#8 OK
    np.deg2rad([18, -50, 63.8, -33, -81.6, 0.2]),#9 OK
    np.deg2rad([51.2, -44.5, 69.2, -25.2, -39.9, 43.4]),#10 OK
    np.deg2rad([48.1, -44.5, 69.2, -25.2, -43, 43.4]),#11 OK
    np.deg2rad([51.2, -44.5, 69.2, -25.2, -39.9, 43.4]),#12 OK
    np.deg2rad([46.5, -37.6, 60.7, -20.6, -42.2, 42.7]),#13 OK
    np.deg2rad([48.1, -37.6, 60.7, -21.4, -42.2, 42.7]),#14 OK
    np.deg2rad([46.5, -37.6, 60.7, -20.6, -42.2, 42.7]),#15 OK
    np.deg2rad([42.7, -45.3, 74.6, -31.4, -48.4, 45]),#16 OK
    np.deg2rad([45, -45.3, 74.6, -31.4, -45.3, 45]),#17 OK
    np.deg2rad([42.7, -45.3, 74.6, -31.4, -48.4, 45]),#18 OK
    np.deg2rad([-15.4, -76.5, 101.9, -115.1, -91.2, 25]),#19
    np.deg2rad([-15.8, -60.6, 114.5, -146.9, -88.5, 31.1]),#20 OK
    np.deg2rad([-15.4, -76.5, 101.9, -115.1, -91.2, 25]),#21 OK
    np.deg2rad([-35.4, -95.1, 129.1, -123, -91.2, 102.8]),#22 OK
    np.deg2rad([-38, -72.6, 145.1, -162.9, -88.5, 97.5]),#23 OK
    np.deg2rad([-35.4, -119, 126.5, -99.1, -88.5, 98.8]),#24 OK
    np.deg2rad([90.8, -71.2, 103.9, -121.7, -92.5, 136]),#25 OK
    np.deg2rad([90.8, -71.2, 103.9, -121.7, -92.5, 136]),#26 OK
    np.deg2rad([88.2, -68.6, 107.9, -129.7, -90.5, 132]),#27 OK
    np.deg2rad([85.5, -68.6, 107.9, -129.7, -91.2, 132]),#28 OK
    np.deg2rad([85.5, -83.2, 91.3, -99.1, -89.8, 132]),#29 OK
    np.deg2rad([185.2, -141.6, 135.1, -173.5, -91.2, 132]),#30 OK
    np.deg2rad([177.2, -93.8, 111.2, -107.1, -91.2, 132]),#31 OK
    np.deg2rad([177.8, -83, 122, -128, -90.6, 132]),#32 OK
    np.deg2rad([185.2, -141.6, 135.1, -173.5, -91.2, 132]),#33 OK
    np.deg2rad([85.5, -89.8, 123.8, -123, -92.5, -48.6]),#34 OK
    np.deg2rad([65.6, -69.9, 101.9, -121.7, -88.5, -69.9]),#35 OK
    np.deg2rad([-35.4, -95.1, 129.1, -123, -91.2, 102.8]),#36 OK
    np.deg2rad([-38, -72.6, 145.1, -162.9, -88.5, 97.5]),#37 OK
    np.deg2rad([-35.4, -95.1, 129.1, -123, -91.2, 102.8]),#38 OK
    np.deg2rad([-67.2, -72.6, 94.6, -111.1, -89.8, 157.3]),#39 OK
    np.deg2rad([-68.5, -61.9, 105.2, -131, -88.5, 157.3]),#40 OK
    np.deg2rad([-67.2, -72.6, 94.6, -111.1, -89.8, 157.3]),#41 OK
    np.deg2rad([-28.7, -46, 58, -103.1, -89.8, 15.1]),#42 OK
    np.deg2rad([-26.1, -44.7, 61.4, -107.1, -89.8, 19.1]),#43 OK
    np.deg2rad([-26.1, -63.3, 75.3, -107.1, -89.8, 19.1]),#44 OK
    np.deg2rad([81.5, -73.9, 105.9, -123, -92.5, 36.4]),#45 OK
    np.deg2rad([78.9, -69.9, 104.5, -124.4, -91.2, 36.4]),#46 OK
    np.deg2rad([77.6, -69.9, 104.5, -124.4, -91.2, 33.7]),#47 OK
    np.deg2rad([81.5, -73.9, 105.9, -123, -92.5, 36.4]),#48 OK
    np.deg2rad([81.5, -73.9, 105.9, -123, -92.5, 36.4]),#49 OK

    np.deg2rad([81.5, -96.5, 103.9, -97.8, -88.5, 132]),#50 OK
    np.deg2rad([-67.2, -72.6, 94.6, -111.1, -89.8, 157.3]),#51 OK
    np.deg2rad([-68.6, -61.9, 105.2, -131, -88.5, 155.9]),#52 OK
    np.deg2rad([-67.2, -72.6, 94.6, -111.1, -89.8, 157.3]),#53 OK
    np.deg2rad([-15.4, -76.5, 101.9, -115.1, -91.2, 25]),#54 OK
    np.deg2rad([-15.8, -60.6, 114.5, -146.9, -88.5, 31.1]),#55 OK
    np.deg2rad([-15.4, -76.5, 101.9, -115.1, -91.2, 25]),#56 OK
    np.deg2rad([82.9, -80.5, 101.9, -115.1, -91.2, 24.4]), #57 OK
    np.deg2rad([85.5, -73.9, 109.2, -123, -91.2, 24.4]),#58 OK
    np.deg2rad([82.9, -80.5, 101.9, -115.1, -91.2, 24.4])#59 OK


]

# 7. 定義時間排程（移動持續時間, 起點姿態, 終點姿態, 等待時間, 使用工具）
motion_schedule = [
    (0.5, target_joint_positions_rad[0], target_joint_positions_rad[1], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[1], target_joint_positions_rad[2], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[2], target_joint_positions_rad[3], 0.0, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[3], target_joint_positions_rad[4], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[4], target_joint_positions_rad[5], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[5], target_joint_positions_rad[6], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[6], target_joint_positions_rad[7], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[7], target_joint_positions_rad[8], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[8], target_joint_positions_rad[9], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[9], target_joint_positions_rad[10], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[10], target_joint_positions_rad[11], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[11], target_joint_positions_rad[12], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[12], target_joint_positions_rad[13], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[13], target_joint_positions_rad[14], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[14], target_joint_positions_rad[15], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[15], target_joint_positions_rad[16], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[16], target_joint_positions_rad[17], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[17], target_joint_positions_rad[18], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[18], target_joint_positions_rad[19], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[19], target_joint_positions_rad[20], 0.1, "No_tool","Tool_1_1_189","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[20], target_joint_positions_rad[21], 0.1, "No_tool","Tool_1_1_189","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[21], target_joint_positions_rad[22], 0.1, "No_tool","Tool_1_1_189","Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[22], target_joint_positions_rad[23], 0.1, "TOOL2_FLAT","Tool_1_1_189","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[23], target_joint_positions_rad[24], 0.1, "TOOL2_FLAT","Tool_1_1_189","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.5, target_joint_positions_rad[24], target_joint_positions_rad[25], 0.1, "TOOL2_FLAT","Tool_1_1_189","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"), #OK
    (0.1, target_joint_positions_rad[25], target_joint_positions_rad[26], 0.1, "TOOL2_FLAT","Tool_1_1_189","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCover_convayer"),  #OK #多於動作，可設定時間最小
    (0.5, target_joint_positions_rad[26], target_joint_positions_rad[27], 0.1, "TOOL2_FLAT","Tool_1_1_189","Tool_3_1_258","C2195_MB_1_289","C2195_UpperCoverOnHand"), #OK
    (0.5, target_joint_positions_rad[27], target_joint_positions_rad[28], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_UpperCoverOnHand"), #OK
    (0.5, target_joint_positions_rad[28], target_joint_positions_rad[29], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_UpperCoverOnHand"), #OK
    (0.5, target_joint_positions_rad[29], target_joint_positions_rad[30], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_UpperCoverOnHand"), #OK
    (0.5, target_joint_positions_rad[30], target_joint_positions_rad[31], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_UpperCoverOnHand"), #OK
    (0.5, target_joint_positions_rad[31], target_joint_positions_rad[32], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[32], target_joint_positions_rad[33], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[33], target_joint_positions_rad[34], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[34], target_joint_positions_rad[35], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[35], target_joint_positions_rad[36], 0.1, "TOOL2_FLAT","Tool_1_1_189", "Tool_3_1_258","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[36], target_joint_positions_rad[37], 0.1, "No_tool","Tool_1_1_189", "Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[37], target_joint_positions_rad[38], 0.1, "No_tool","Tool_1_1_189", "Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[38], target_joint_positions_rad[39], 0.1, "No_tool","Tool_1_1_189", "Tool_2_1_240","Tool_3_1_258","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[39], target_joint_positions_rad[40], 0.1, "TOOL3_FLAT","Tool_1_1_189", "Tool_2_1_240","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[40], target_joint_positions_rad[41], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[41], target_joint_positions_rad[42], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195_MB_1_289","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[42], target_joint_positions_rad[43], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195_MB_OnHand","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[43], target_joint_positions_rad[44], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195_MB_OnHand","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[44], target_joint_positions_rad[45], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195_MB_OnHand","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[45], target_joint_positions_rad[46], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195_MB_OnHand","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[46], target_joint_positions_rad[47], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[47], target_joint_positions_rad[48], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.01, target_joint_positions_rad[48], target_joint_positions_rad[49], 0.01, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[49], target_joint_positions_rad[50], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[50], target_joint_positions_rad[51], 0.1, "TOOL3_FLAT","Tool_1_1_189","Tool_2_1_240","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[51], target_joint_positions_rad[52], 0.1, "No_tool","Tool_3_1_258","Tool_1_1_189","Tool_2_1_240","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[52], target_joint_positions_rad[53], 0.1, "No_tool","Tool_3_1_258","Tool_1_1_189","Tool_2_1_240","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[53], target_joint_positions_rad[54], 0.1, "No_tool","Tool_3_1_258","Tool_1_1_189","Tool_2_1_240","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[54], target_joint_positions_rad[55], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[55], target_joint_positions_rad[56], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[56], target_joint_positions_rad[57], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195MB","C2195_Upper_cover_1_290"), #OKOK
    (0.5, target_joint_positions_rad[57], target_joint_positions_rad[58], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195MB","C2195_Upper_cover_1_290"), #OK
    (0.5, target_joint_positions_rad[58], target_joint_positions_rad[59], 0.1, "TOOL1_FLAT","Tool_2_1_240","Tool_3_1_258","C2195MB","C2195_Upper_cover_1_290") #OK

]

# 8. 控制旗標
import time
start_sim_time = None
start_wall_time = None
current_phase = 0
play_motion = False
pause_motion = False
reset_requested = False
move_timer = 0.0
wait_timer = 0.0
in_waiting_phase = False
ct_reported = False

# 8-1. 播放控制函式
def on_play():
    global play_motion, pause_motion
    play_motion = True
    pause_motion = False
    print("▶️ PLAY")

def on_pause():
    global pause_motion
    pause_motion = True
    print("⏸ PAUSE")

def on_reset():
    global reset_requested, start_sim_time, start_wall_time
    global current_phase, move_timer, wait_timer, in_waiting_phase
    reset_requested = True
    start_sim_time = None
    start_wall_time = None
    current_phase = 0
    move_timer = 0.0
    wait_timer = 0.0
    in_waiting_phase = False
    print("🔁 RESTART")

# 8-0. 額外物件路徑定義
ALL_OBJECTS = {

    #手臂上的主板
    "C2195_MB_OnHand": "/World/ur20/wrist_3_link/flange/TOOL3_FLAT/Tool_3/C2195_MB_OnHand", #OK
    #等待區的主板
    "C2195_MB_1_289": "/World/Wiwynn_WorkStation_material_01/Wiwynn_WorkStation/Geometry/__0/C2195_MB_1_289", #OK
    #工作區的主板
    "C2195MB": "/World/Wiwynn_WorkStation_material_01/Wiwynn_WorkStation/Geometry/__0/C2195_chassis_1_288/C2195MB",#OK

    #等待區的上蓋
    "C2195_Upper_cover_1_290": "/World/Wiwynn_WorkStation_material_01/Wiwynn_WorkStation/Geometry/__0/C2195_Upper_cover_1_290",#OK
    #手臂上的上蓋
    "C2195_UpperCoverOnHand": "/World/ur20/wrist_3_link/flange/TOOL2_FLAT/Tool_2/C2195_UpperCoverOnHand",#OK
    #工作區的上蓋
    "C2195_UpperCover_convayer": "/World/Wiwynn_WorkStation_material_01/Wiwynn_WorkStation/Geometry/__0/C2195_chassis_1_288/C2195_UpperCover_convayer", #OK
    
    #等待區的三組工具
    "Tool_1_1_189": "/World/Wiwynn_WorkStation_material_01/Wiwynn_WorkStation/Geometry/__0/Tool_1_1_189", #OK
    "Tool_2_1_240": "/World/Wiwynn_WorkStation_material_01/Wiwynn_WorkStation/Geometry/__0/Tool_2_1_240", #OK
    "Tool_3_1_258": "/World/Wiwynn_WorkStation_material_01/Wiwynn_WorkStation/Geometry/__0/Tool_3_1_258" #OK
}


# 9. UI 控制與畫面
window = ui.Window("UR20 Controller", width=360, height=540)
with window.frame:
    with ui.VStack(spacing=5):
        ui.Button("Play", clicked_fn=on_play)
        ui.Button("Pause", clicked_fn=on_pause)
        ui.Button("Restart", clicked_fn=on_reset)
        status_label = ui.Label("Waiting for input...", alignment=ui.Alignment.CENTER)

        joint_labels = [ui.Label(f"Joint {i+1}: 0.0°") for i in range(6)]

        phase_range = f"Phase 0~{len(motion_schedule)-1}, enter your phase"
        ui.Label(phase_range)
        phase_input = ui.StringField()
        def on_go_phase():
            global current_phase, move_timer, wait_timer, in_waiting_phase
            try:
                val = int(phase_input.model.get_value_as_string())
                if 0 <= val < len(motion_schedule):
                    current_phase = val
                    move_timer = 0.0
                    wait_timer = 0.0
                    in_waiting_phase = False
                    status_label.text = f"Jump to Phase {val}"
                else:
                    status_label.text = f"❌ Invalid Phase: {val}"
            except:
                status_label.text = "❌ Invalid input"
        ui.Button("Go Phase", clicked_fn=on_go_phase)

        ui.Label("Set Joint Angles (degrees):")
        joint_inputs = [ui.StringField() for _ in range(6)]
        def on_apply_joints():
            try:
                angles_deg = [float(j.model.get_value_as_string()) for j in joint_inputs]
                angles_rad = np.deg2rad(angles_deg)
                ur20.set_joint_positions(angles_rad)
                status_label.text = f"✅ Applied angles: {angles_deg}"
            except:
                status_label.text = "❌ Invalid joint input"
        ui.Button("Apply Joints", clicked_fn=on_apply_joints)

# 10. 每一幀更新
def on_update(e):
    global start_sim_time, start_wall_time, current_phase, play_motion, pause_motion
    global reset_requested, move_timer, wait_timer, in_waiting_phase, ct_reported

    if not play_motion or pause_motion:
        return

    if reset_requested:
        reset_requested = False
        ur20.set_joint_positions(motion_schedule[0][1])
        return

    if start_sim_time is None:
        start_sim_time = world.current_time
        start_wall_time = time.time()
        ur20.set_joint_positions(motion_schedule[0][1])

        # 初始只顯示 TOOL1_FLAT，其它隱藏
        default_tool = "TOOL1_FLAT"
        for tool in ["TOOL1_FLAT", "TOOL2_FLAT", "TOOL3_FLAT", "TOOL4_FLAT", "TOOL5_FLAT"]:
            prim = stage.GetPrimAtPath(f"/World/ur20/wrist_3_link/flange/{tool}")
            if prim.IsValid():
                attr = prim.GetAttribute("visibility")
                attr.Set("inherited" if tool == default_tool else "invisible")
        # 額外物件初始化
        for obj in ALL_OBJECTS.values():
            prim = stage.GetPrimAtPath(obj)
            if prim.IsValid():
                prim.GetAttribute("visibility").Set("invisible")

        status_label.text = "Start simulation..."
        return

    delta_time = world.get_physics_dt()
    joint_angles = ur20.get_joint_positions()
    for i in range(6):
        deg = np.rad2deg(joint_angles[i])
        joint_labels[i].text = f"Joint {i+1}: {deg:.1f}°"

    if current_phase < len(motion_schedule):
        move_duration, pose_start, pose_end, wait_duration, tool_to_show, *extra_objs = motion_schedule[current_phase]

        if not in_waiting_phase:
            move_timer += delta_time
            alpha = min(move_timer / move_duration, 1.0)
            ur20.set_joint_positions((1 - alpha) * pose_start + alpha * pose_end)

            if move_timer >= move_duration:
                # 工具切換
                for tool in ["TOOL1_FLAT", "TOOL2_FLAT", "TOOL3_FLAT", "TOOL4_FLAT", "TOOL5_FLAT"]:
                    prim = stage.GetPrimAtPath(f"/World/ur20/wrist_3_link/flange/{tool}")
                    if prim.IsValid():
                        attr = prim.GetAttribute("visibility")
                        attr.Set("inherited" if tool == tool_to_show else "invisible")

                # 額外 3D 物件切換
                show_set = set(extra_objs)
                for name, path in ALL_OBJECTS.items():
                    prim = stage.GetPrimAtPath(path)
                    if prim.IsValid():
                        prim.GetAttribute("visibility").Set("inherited" if name in show_set else "invisible")

                move_timer = 0.0
                in_waiting_phase = True
                msg = f"Phase {current_phase} wait {wait_duration} sec, Show {tool_to_show}, Objects: {extra_objs}"
                print(msg)
                status_label.text = msg

        else:
            wait_timer += delta_time
            if wait_timer >= wait_duration:
                current_phase += 1
                wait_timer = 0.0
                in_waiting_phase = False
                if current_phase < len(motion_schedule):
                    status_label.text = f"Enter Phase {current_phase} [{current_phase-1}→{current_phase}]"
                else:
                    status_label.text = "✅ All phases complete."

    elif not ct_reported:
        ct_reported = True
        ct = time.time() - start_wall_time
        msg = f"✅ Motion complete! C/T = {ct:.2f} sec"
        print(msg)
        status_label.text = msg

# 11. 主迴圈
while simulation_app.is_running():
    simulation_app.update()
    on_update(None)

# 12. 關閉
simulation_app.close()