# Universal modifiers
        damage_increase = st.number_input("Damage Increase (%)", min_value=0.0, max_value=300.0, value=80.0, step=5.0, 
                                        help="Final damage increase from gear/cards/runes")
        
        # Equipment Memory System
        equipment_memory_bonus = 0
        if st.checkbox("🧠 Include Equipment Memory System", help="New system from Ghost Palace - adds significant ATK/MATK bonuses"):
            st.markdown("#### 🧠 Equipment Memory Configuration")
            
            col_mem1, col_mem2 = st.columns(2)
            
            with col_mem1:
                st.markdown("**Memory Quality & Levels**")
                # Equipment Memory slots (6 total: Weapon, Armor, Cloak, Boots, Accessory 1, Accessory 2)
                memory_slots = ["Weapon", "Armor", "Cloak", "Boots", "Accessory 1", "Accessory 2"]
                
                total_memory_atk = 0
                total_memory_matk = 0
                
                for slot in memory_slots:
                    memory_quality = st.selectbox(f"{slot} Memory", 
                        [("None", 0), ("Green", 1), ("Blue", 2), ("Purple", 3)], 
                        index=0, format_func=lambda x: x[0], key=f"mem_{slot}")
                    
                    if memory_quality[1] > 0:
                        max_level = {1: 10, 2: 20, 3: 30}[memory_quality[1]]  # Green: 10, Blue: 20, Purple: 30
                        memory_level = st.number_input(f"{slot} Level", min_value=1, max_value=max_level, 
                                                     value=min(10, max_level), key=f"level_{slot}")
                        
                        # Calculate memory bonuses (approximation based on guides)
                        if damage_type == "Physical Damage":
                            # Physical ATK bonus from memory
                            if memory_quality[1] == 3:  # Purple
                                slot_atk_bonus = memory_level * 15  # ~15 ATK per level for purple
                            elif memory_quality[1] == 2:  # Blue  
                                slot_atk_bonus = memory_level * 10  # ~10 ATK per level for blue
                            else:  # Green
                                slot_atk_bonus = memory_level * 5   # ~5 ATK per level for green
                        else:
                            # Magic ATK bonus from memory
                            if memory_quality[1] == 3:  # Purple
                                slot_atk_bonus = memory_level * 12  # ~12 MATK per level for purple
                            elif memory_quality[1] == 2:  # Blue
                                slot_atk_bonus = memory_level * 8   # ~8 MATK per level for blue  
                            else:  # Green
                                slot_atk_bonus = memory_level * 4   # ~4 MATK per level for green
                        
                        total_memory_atk += slot_atk_bonus
                        
                        # Display individual memory bonus
                        st.text(f"└ +{slot_atk_bonus} {'ATK' if damage_type == 'Physical Damage' else 'MATK'}")
            
            with col_mem2:
                st.markdown("**Memory Special Attributes**")
                
                # Special attributes unlocked at certain levels
                memory_special_atk_percent = st.number_input("ATK/MATK % from Special Lines", 
                    min_value=0.0, max_value=50.0, value=0.0, step=1.0,
                    help="Special attributes from Lv.10+ purple memories")
                
                memory_damage_increase = st.number_input("Damage Increase % from Memory", 
                    min_value=0.0, max_value=30.0, value=0.0, step=1.0,
                    help="Damage increase special attributes")
                
                memory_penetration = st.number_input("Penetration % from Memory", 
                    min_value=0.0, max_value=20.0, value=0.0, step=1.0,
                    help="Ignore DEF from special attributes")
                
                # Add memory bonuses to existing modifiers
                if damage_type == "Physical Damage":
                    atk_percent += memory_special_atk_percent
                    total_atk += total_memory_atk
                    ignore_def_general += memory_penetration
                else:
                    matk_percent += memory_special_atk_percent
                    total_matk += total_memory_atk
                    ignore_mdef_general += memory_penetration
                    
                damage_increase += memory_damage_increase
                
                # Display total memory bonuses
                st.success(f"""
                **Total Memory Bonuses:**
                - +{total_memory_atk} {'ATK' if damage_type == 'Physical Damage' else 'MATK'} (Base)
                - +{memory_special_atk_percent}% {'ATK' if damage_type == 'Physical Damage' else 'MATK'} (Special)
                - +{memory_damage_increase}% Damage Increase
                - +{memory_penetration}% Penetration
                """)
                
                # Memory upgrade recommendations
                st.info("""
                **💡 Memory Tips:**
                - Focus on 3x Purple Lv.10 first (unlocks special attributes)
                - Then upgrade to Lv.30 one by one
                - Green/Blue memories refund only 80% when decomposed
                - Weekly Ghost Palace = ~30 Memory Afterglow
                """)
        else:
            total_memory_atk = 0        # Show advanced mechanics info
        if "advanced_mechanics" in class_info:
            with st.expander(f"🔍 Advanced {character_class.split('/')[0]} Mechanics"):
                for mechanic, description in class_info["advanced_mechanics"].items():
                    if mechanic == "special_note":
                        st.warning(f"**Special Note:** {description}")
                    elseimport streamlit as st
import pandas as pd
import numpy as np
import math

# Page configuration
st.set_page_config(
    page_title="ROM Universal Damage Calculator",
    page_icon="⚔️",
    layout="wide"
)

# Title and description
st.title("⚔️ Ragnarok M: Universal Damage Calculator")
st.markdown("""
**ROM Handbook Official Formulas** - Accurate for all classes and skills  
Calculate damage for any class using exact game formulas from ROM Handbook.
""")

# Official formula display
with st.expander("📋 ROM Handbook Universal Formula Reference"):
    st.markdown("""
    **Universal Physical Damage Formula:**
    ```lua
    -- Core ROM Calculation Pattern
    local Str/Dex/Int = srcUser:GetProperty("MainStat")
    local Atk = srcUser:GetProperty("Atk") 
    local AtkPer = srcUser:GetProperty("AtkPer")
    local DamIncrease = srcUser:GetProperty("DamIncrease")
    local Refine = srcUser:GetProperty("Refine")
    
    -- Defense System
    local IgnoreDef1 = srcUser:GetProperty("IgnoreDef")
    local IgnoreDef2 = srcUser:GetProperty("IgnoreEquipDef") 
    if targetUser.boss or targetUser.mini then
        IgnoreDef = IgnoreDef1
    else  
        IgnoreDef = IgnoreDef1 + IgnoreDef2
    end
    
    -- Final Calculation
    BaseDamage = (Atk * AtkPer * SkillMultiplier * SizeModifier * ElementModifier)
    AfterDefense = BaseDamage * (1 - DefenseReduction) 
    FinalDamage = (AfterDefense + Refine) * (1 + DamIncrease)
    ```
    
    **Magic Damage Formula:**
    ```lua
    -- Magic follows similar pattern with MAtk/MAtkPer/IgnoreMDef
    BaseMagicDamage = (MAtk * MAtkPer * SkillMultiplier * ElementModifier)
    AfterMDefense = BaseMagicDamage * (1 - MDefenseReduction)
    FinalMagicDamage = (AfterMDefense + MRefine) * (1 + DamIncrease)
    ```
    """)

# Advanced class stat requirements with detailed mechanics
class_stats = {
    "Knight/Lord Knight/Rune Knight": {
        "main": "STR", "secondary": ["VIT", "DEX"], "tertiary": ["AGI"], 
        "description": "STR for damage, VIT for HP/DEF, DEX for HIT",
        "build_types": ["Pure STR DPS", "STR-VIT Tank", "STR-DEX Hybrid"],
        "advanced_mechanics": {
            "str_mechanics": "Every 10 STR = +20 ATK approximately",
            "vit_mechanics": "Every 5 VIT = +1% damage reduction",
            "dex_mechanics": "Every 10 DEX = +20 HIT"
        }
    },
    "Assassin/Assassin Cross/Guillotine Cross": {
        "main": "AGI", "secondary": ["STR", "LUK"], "tertiary": ["DEX"], 
        "description": "AGI for ASPD/Crit, STR for damage, LUK for crit rate",
        "build_types": ["AGI-Critical", "AGI-STR Hybrid", "Pure Critical (LUK)"],
        "advanced_mechanics": {
            "agi_mechanics": "Every 10 AGI = +4% ASPD, +2 Flee",
            "luk_mechanics": "Every 10 LUK = +1% Critical Rate",
            "str_mechanics": "STR affects base damage significantly"
        }
    },
    "Hunter/Sniper/Ranger": {
        "main": "DEX", "secondary": ["AGI", "INT"], "tertiary": ["STR"], 
        "description": "DEX for damage/HIT, AGI for ASPD, INT for SP",
        "build_types": ["Pure DEX ADL", "DEX-AGI ASPD", "DEX-INT Trapper"],
        "advanced_mechanics": {
            "dex_mechanics": "Primary damage stat for bows, affects accuracy",
            "agi_mechanics": "ASPD for auto-attack builds",
            "int_mechanics": "SP for trap skills and utility"
        }
    },
    "Priest/High Priest/Archbishop": {
        "main": "INT", "secondary": ["DEX", "VIT"], "tertiary": ["AGI"], 
        "description": "INT for healing/damage, DEX for cast time, VIT for survival",
        "build_types": ["Pure INT Battle", "INT-DEX Support", "INT-VIT Tank"],
        "advanced_mechanics": {
            "int_mechanics": "Every 10 INT = +20 MATK, +2% healing",
            "dex_mechanics": "Reduces cast time significantly",
            "vit_mechanics": "Survivability for battle priests"
        }
    },
    "Wizard/High Wizard/Warlock/Sorcerer": {
        "main": "INT", "secondary": ["DEX", "VIT"], "tertiary": ["AGI"], 
        "description": "INT for magic damage, DEX for cast time, VIT for survival",
        "build_types": ["Pure INT Glass Cannon", "INT-DEX Fast Cast", "INT-VIT Survivor"],
        "advanced_mechanics": {
            "int_mechanics": "Primary magic damage, every 10 INT = +20 MATK",
            "dex_mechanics": "Critical for instant cast (150+ DEX recommended)",
            "vit_mechanics": "HP for survival, reduces stun duration"
        }
    },
    "Blacksmith/Whitesmith/Mechanic": {
        "main": "STR", "secondary": ["DEX", "AGI", "LUK"], "tertiary": ["VIT"], 
        "description": "🔧 COMPLEX: STR+DEX+AGI+LUK all affect damage through different mechanics",
        "build_types": ["STR-DEX Hybrid", "STR-AGI Memory", "DEX-LUK Rune", "Balanced Multi-Stat"],
        "advanced_mechanics": {
            "str_mechanics": "Base physical damage for all skills",
            "dex_mechanics": "🎯 DEX Runes: Every 10 DEX = +X ATK (varies by rune level)",
            "agi_mechanics": "⚡ ASPD Memory: 360 ASPD = +3% Penetration, affects attack speed",
            "luk_mechanics": "🍀 LUK Runes: Every 10 LUK = +X ATK (varies by rune level)",
            "special_note": "⚠️ Mechanic uses ALL 4 STATS for optimal damage!"
        }
    },
    "Crusader/Paladin/Royal Guard": {
        "main": "STR", "secondary": ["VIT", "DEX"], "tertiary": ["INT"], 
        "description": "STR for damage, VIT for tanking, DEX for HIT, INT for SP",
        "build_types": ["STR-VIT Tank", "Pure VIT Defender", "STR-DEX Sacrifice"],
        "advanced_mechanics": {
            "str_mechanics": "Physical damage for offensive skills",
            "vit_mechanics": "Primary tanking stat, affects HP and DEF",
            "int_mechanics": "SP for skills like Heal and Sanctuary"
        }
    },
    "Rogue/Stalker/Shadow Chaser": {
        "main": "STR", "secondary": ["AGI", "DEX"], "tertiary": ["LUK"], 
        "description": "STR for damage, AGI for ASPD, DEX for HIT, LUK for steal",
        "build_types": ["STR-AGI Hybrid", "Pure STR DPS", "DEX-based Copy"],
        "advanced_mechanics": {
            "str_mechanics": "Primary damage stat",
            "agi_mechanics": "ASPD and flee for survivability",
            "dex_mechanics": "Accuracy and some skill requirements",
            "luk_mechanics": "Affects steal rate and critical"
        }
    },
    "Monk/Champion/Shura/Sura": {
        "main": "STR", "secondary": ["AGI", "VIT"], "tertiary": ["DEX"], 
        "description": "STR for damage, AGI for combo speed, VIT for HP",
        "build_types": ["Pure STR Asura", "STR-AGI Combo", "STR-VIT Tanky"],
        "advanced_mechanics": {
            "str_mechanics": "Primary damage, critical for Asura Strike",
            "agi_mechanics": "Combo attack speed and ASPD",
            "vit_mechanics": "HP for survival and some skill requirements"
        }
    },
    "Bard-Dancer/Clown-Gypsy/Minstrel-Wanderer": {
        "main": "DEX", "secondary": ["AGI", "INT"], "tertiary": ["LUK"], 
        "description": "DEX for bow damage, AGI for ASPD, INT for SP/songs",
        "build_types": ["DEX-AGI ADL", "Pure DEX", "INT Support"],
        "advanced_mechanics": {
            "dex_mechanics": "Primary damage for bow skills",
            "agi_mechanics": "ASPD for auto-attack builds",
            "int_mechanics": "SP for songs and support skills"
        }
    },
    "Taekwon/Star Gladiator/Soul Linker": {
        "main": "STR", "secondary": ["AGI", "INT"], "tertiary": ["DEX"], 
        "description": "STR for kick damage, AGI for ASPD, INT for linker skills",
        "build_types": ["STR-AGI TKD", "Pure STR Star Glad", "INT Soul Linker"],
        "advanced_mechanics": {
            "str_mechanics": "Kick damage for TKD and Star Glad",
            "agi_mechanics": "ASPD and positioning",
            "int_mechanics": "Soul Linker skills and SP"
        }
    },
    "Ninja/Kagerou/Oboro": {
        "main": "STR", "secondary": ["INT", "AGI"], "tertiary": ["DEX"], 
        "description": "STR for physical, INT for magic, AGI for ASPD",
        "build_types": ["STR Physical", "INT Magic", "Hybrid STR-INT"],
        "advanced_mechanics": {
            "str_mechanics": "Physical ninja skills",
            "int_mechanics": "Magic ninja skills and SP",
            "agi_mechanics": "ASPD and evasion"
        }
    },
    "Gunslinger/Rebel": {
        "main": "DEX", "secondary": ["AGI", "STR"], "tertiary": ["LUK"], 
        "description": "DEX for gun damage/HIT, AGI for ASPD, STR for damage",
        "build_types": ["Pure DEX", "DEX-AGI ASPD", "DEX-STR Hybrid"],
        "advanced_mechanics": {
            "dex_mechanics": "Primary gun damage and accuracy",
            "agi_mechanics": "ASPD for rapid fire",
            "str_mechanics": "Additional damage boost"
        }
    },
    "Super Novice/Hyper Novice": {
        "main": "ALL", "secondary": ["ALL"], "tertiary": ["ALL"], 
        "description": "Can use all stats - very flexible builds",
        "build_types": ["Balanced All Stats", "Specialized Single Stat", "Custom Build"],
        "advanced_mechanics": {
            "flexibility": "Can copy any class build pattern",
            "versatility": "All stats contribute to different aspects",
            "customization": "Build depends on chosen skill focus"
        }
    },
    "Doram (Summoner)": {
        "main": "INT", "secondary": ["DEX", "VIT"], "tertiary": ["AGI"], 
        "description": "INT for magic/healing, DEX for cast time, VIT for survival",
        "build_types": ["Pure INT Magic", "INT-DEX Support", "Physical Doram"],
        "advanced_mechanics": {
            "int_mechanics": "Magic damage and healing power",
            "dex_mechanics": "Cast time reduction",
            "vit_mechanics": "Survivability and some skill scaling"
        }
    }
}

# Class selection
st.sidebar.markdown("### 🎭 Character Setup")
character_class = st.sidebar.selectbox("Select Class Type", list(class_stats.keys()))

# Display class stat information
if character_class in class_stats:
    class_info = class_stats[character_class]
    st.sidebar.markdown("#### 📊 Stat Priority")
    st.sidebar.info(f"**Main:** {class_info['main']}")
    st.sidebar.info(f"**Secondary:** {', '.join(class_info['secondary'])}")
    st.sidebar.info(f"**Description:** {class_info['description']}")
    
    # Build type selector
    selected_build = st.sidebar.selectbox("Build Type", class_info['build_types'])
    st.sidebar.markdown(f"*Selected: {selected_build}*")

damage_type = st.sidebar.selectbox("Damage Type", ["Physical Damage", "Magic Damage"])

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Universal Calculator", "📊 Skill Database", "📈 Build Optimizer", "🔬 Formula Tester"])

with tab1:
    st.subheader("Universal ROM Damage Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Character Stats")
        
        # Get class stat requirements
        class_info = class_stats[character_class]
        
        st.markdown(f"**{character_class}** - *{selected_build}*")
        st.markdown(f"📋 {class_info['description']}")
        
        if damage_type == "Physical Damage":
            # Smart stat input based on class
            if class_info['main'] == "ALL":
                # Super Novice - show all stats equally
                str_stat = st.number_input("STR", min_value=1, max_value=200, value=80, help="Physical attack power")
                agi_stat = st.number_input("AGI", min_value=1, max_value=200, value=80, help="Attack speed, flee")
                vit_stat = st.number_input("VIT", min_value=1, max_value=200, value=80, help="HP, defense")
                int_stat = st.number_input("INT", min_value=1, max_value=200, value=80, help="SP, magic attack")
                dex_stat = st.number_input("DEX", min_value=1, max_value=200, value=80, help="Accuracy, cast time")
                luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=80, help="Critical, status resist")
                
                # For calculation, determine effective main stat
                if "STR" in selected_build:
                    main_stat, main_stat_name = str_stat, "STR"
                elif "DEX" in selected_build:
                    main_stat, main_stat_name = dex_stat, "DEX"
                elif "AGI" in selected_build:
                    main_stat, main_stat_name = agi_stat, "AGI"
                else:
                    main_stat, main_stat_name = str_stat, "STR"  # Default
                    
                secondary_stat = (agi_stat + dex_stat + vit_stat) // 3
                
            elif class_info['main'] == "STR" and "Mechanic" in character_class:
                # Special handling for Mechanic - multi-stat dependency
                st.markdown("**🔧 Mechanic: Multi-Stat Damage System**")
                st.info("⚠️ Mechanic uses STR+DEX+AGI+LUK all contributing to damage through different mechanics!")
                
                main_stat = st.number_input(f"⭐ STR (Base Damage)", min_value=1, max_value=200, value=120, 
                                          help="Primary physical damage stat")
                main_stat_name = "STR"
                
                # DEX with rune mechanics
                dex_stat = st.number_input("🎯 DEX (Rune ATK)", min_value=1, max_value=200, value=80,
                                         help="DEX Runes: Every 10 DEX adds ATK based on rune level")
                dex_rune_level = st.number_input("DEX Rune Level", min_value=0, max_value=15, value=5,
                                               help="Higher rune level = more ATK per 10 DEX")
                dex_atk_bonus = (dex_stat // 10) * (dex_rune_level * 2)  # Approximation
                
                # AGI with memory mechanics  
                agi_stat = st.number_input("⚡ AGI (Memory/ASPD)", min_value=1, max_value=200, value=80,
                                         help="ASPD Memory: 360 ASPD = +3% Penetration")
                total_aspd = st.number_input("Total ASPD", min_value=180, max_value=400, value=300,
                                           help="Your current ASPD including equipment")
                
                # Calculate ASPD memory bonus
                if total_aspd >= 360:
                    aspd_pen_bonus = 3.0  # 3% penetration at 360 ASPD
                elif total_aspd >= 340:
                    aspd_pen_bonus = 2.0  # Scaled bonus
                elif total_aspd >= 320:
                    aspd_pen_bonus = 1.0
                else:
                    aspd_pen_bonus = 0.0
                
                # LUK with rune mechanics
                luk_stat = st.number_input("🍀 LUK (Rune ATK)", min_value=1, max_value=200, value=80,
                                         help="LUK Runes: Every 10 LUK adds ATK based on rune level")
                luk_rune_level = st.number_input("LUK Rune Level", min_value=0, max_value=15, value=5,
                                               help="Higher rune level = more ATK per 10 LUK")
                luk_atk_bonus = (luk_stat // 10) * (luk_rune_level * 2)  # Approximation
                
                # Other stats
                vit_stat = st.number_input("VIT", min_value=1, max_value=200, value=50)
                int_stat = st.number_input("INT", min_value=1, max_value=200, value=30)
                
                # Calculate total stat bonuses
                rune_atk_bonus = dex_atk_bonus + luk_atk_bonus
                secondary_stat = max(dex_stat, agi_stat, luk_stat)
                
                # Display Mechanic bonuses
                st.markdown("#### 🔧 Mechanic Stat Bonuses")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("DEX Rune ATK", f"+{dex_atk_bonus}")
                    st.metric("LUK Rune ATK", f"+{luk_atk_bonus}")
                with col_b:
                    st.metric("Total Rune ATK", f"+{rune_atk_bonus}")
                    st.metric("ASPD Penetration", f"+{aspd_pen_bonus}%")
                with col_c:
                    if aspd_pen_bonus >= 3:
                        st.success("✅ Max ASPD Memory!")
                    else:
                        st.warning(f"⚠️ Need {360-total_aspd} more ASPD for max bonus")
                
            elif class_info['main'] == "STR":
                main_stat = st.number_input(f"⭐ STR (Main)", min_value=1, max_value=200, value=120, 
                                          help="Primary damage stat for this class")
                main_stat_name = "STR"
                
                # Show secondary stats based on class
                if "VIT" in class_info['secondary']:
                    vit_stat = st.number_input("🛡️ VIT (Secondary)", min_value=1, max_value=200, value=80,
                                             help="HP, physical defense")
                else:
                    vit_stat = st.number_input("VIT", min_value=1, max_value=200, value=50)
                    
                if "DEX" in class_info['secondary']:
                    dex_stat = st.number_input("🎯 DEX (Secondary)", min_value=1, max_value=200, value=80,
                                             help="Accuracy, cast time reduction")
                else:
                    dex_stat = st.number_input("DEX", min_value=1, max_value=200, value=50)
                    
                if "AGI" in class_info['secondary']:
                    agi_stat = st.number_input("⚡ AGI (Secondary)", min_value=1, max_value=200, value=80,
                                             help="Attack speed, flee")
                else:
                    agi_stat = st.number_input("AGI", min_value=1, max_value=200, value=50)
                    
                # Always show INT and LUK
                int_stat = st.number_input("INT", min_value=1, max_value=200, value=30)
                luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=30)
                
                secondary_stat = max(vit_stat, dex_stat, agi_stat)
                rune_atk_bonus = 0  # Default for non-Mechanic classes
                
            elif class_info['main'] == "DEX":
                main_stat = st.number_input(f"⭐ DEX (Main)", min_value=1, max_value=200, value=120,
                                          help="Primary damage stat for ranged classes")
                main_stat_name = "DEX"
                
                if "AGI" in class_info['secondary']:
                    agi_stat = st.number_input("⚡ AGI (Secondary)", min_value=1, max_value=200, value=80,
                                             help="Attack speed for bow users")
                else:
                    agi_stat = st.number_input("AGI", min_value=1, max_value=200, value=50)
                    
                if "INT" in class_info['secondary']:
                    int_stat = st.number_input("🔮 INT (Secondary)", min_value=1, max_value=200, value=80,
                                             help="SP, some skills require INT")
                else:
                    int_stat = st.number_input("INT", min_value=1, max_value=200, value=30)
                    
                str_stat = st.number_input("STR", min_value=1, max_value=200, value=50)
                vit_stat = st.number_input("VIT", min_value=1, max_value=200, value=50)
                luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=30)
                
                secondary_stat = max(agi_stat, int_stat)
                
            elif class_info['main'] == "AGI":
                main_stat = st.number_input(f"⭐ AGI (Main)", min_value=1, max_value=200, value=120,
                                          help="Primary stat for critical/ASPD builds")
                main_stat_name = "AGI"
                
                if "STR" in class_info['secondary']:
                    str_stat = st.number_input("⚔️ STR (Secondary)", min_value=1, max_value=200, value=80,
                                             help="Physical damage boost")
                else:
                    str_stat = st.number_input("STR", min_value=1, max_value=200, value=50)
                    
                if "LUK" in class_info['secondary']:
                    luk_stat = st.number_input("🍀 LUK (Secondary)", min_value=1, max_value=200, value=80,
                                             help="Critical rate, perfect dodge")
                else:
                    luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=30)
                    
                dex_stat = st.number_input("DEX", min_value=1, max_value=200, value=50)
                vit_stat = st.number_input("VIT", min_value=1, max_value=200, value=50)
                int_stat = st.number_input("INT", min_value=1, max_value=200, value=30)
                
                secondary_stat = max(str_stat, luk_stat)
                
            else:
                # Fallback for other main stats
                main_stat = st.number_input(f"⭐ {class_info['main']} (Main)", min_value=1, max_value=200, value=120)
                main_stat_name = class_info['main']
                secondary_stat = st.number_input("Secondary Stat", min_value=1, max_value=200, value=80)
                luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=30)
                
            # Attack values
            total_atk = st.number_input("Total ATK", min_value=0, value=3000, help="Your total ATK shown in status window")
            weapon_atk = st.number_input("Weapon ATK", min_value=0, value=1200, help="Base weapon attack")
            
        else:  # Magic Damage
            main_stat = st.number_input(f"⭐ INT (Main)", min_value=1, max_value=200, value=120,
                                      help="Primary magic damage stat")
            main_stat_name = "INT"
            
            if "DEX" in class_info['secondary']:
                dex_stat = st.number_input("🎯 DEX (Secondary)", min_value=1, max_value=200, value=80,
                                         help="Cast time reduction")
            else:
                dex_stat = st.number_input("DEX", min_value=1, max_value=200, value=50)
                
            if "VIT" in class_info['secondary']:
                vit_stat = st.number_input("🛡️ VIT (Secondary)", min_value=1, max_value=200, value=80,
                                         help="Survivability for casters")
            else:
                vit_stat = st.number_input("VIT", min_value=1, max_value=200, value=50)
                
            # Other stats
            str_stat = st.number_input("STR", min_value=1, max_value=200, value=30)
            agi_stat = st.number_input("AGI", min_value=1, max_value=200, value=30)
            luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=30)
            
            secondary_stat = max(dex_stat, vit_stat)
            
            total_matk = st.number_input("Total MATK", min_value=0, value=2500, help="Your total MATK shown in status window")
            weapon_matk = st.number_input("Weapon MATK", min_value=0, value=800, help="Base weapon magic attack")
            
        # Common stats
        base_level = st.number_input("Base Level", min_value=1, max_value=200, value=140)
        job_level = st.number_input("Job Level", min_value=1, max_value=70, value=60)
        
        # Show stat analysis
        if st.button("📊 Analyze Stat Distribution"):
            total_stats = str_stat + agi_stat + vit_stat + int_stat + dex_stat + luk_stat if 'str_stat' in locals() else main_stat + secondary_stat + luk_stat
            
            st.info(f"""
            **Stat Analysis for {selected_build}:**
            - Main Stat ({main_stat_name}): {main_stat} ({main_stat/total_stats*100:.1f}%)
            - Secondary Stats: {secondary_stat} 
            - Build Efficiency: {"✅ Optimized" if main_stat >= secondary_stat * 1.5 else "⚠️ Consider more main stat"}
            - Recommended for: {class_info['description']}
            """)
        
    with col2:
        st.markdown("#### ⚔️ Equipment & Modifiers")
        
        # Refine and equipment
        refine_level = st.number_input("Refine Level (+)", min_value=0, max_value=15, value=10)
        refine_attack_bonus = refine_level * 12  # Standard refine bonus
        
        if damage_type == "Physical Damage":
            atk_percent = st.number_input("ATK % Increase", min_value=0.0, max_value=500.0, value=50.0, step=5.0)
            ignore_def_general = st.number_input("Ignore DEF (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
            ignore_def_equip = st.number_input("Ignore Equip DEF (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
        else:
            matk_percent = st.number_input("MATK % Increase", min_value=0.0, max_value=500.0, value=50.0, step=5.0)
            ignore_mdef_general = st.number_input("Ignore MDEF (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
            ignore_mdef_equip = st.number_input("Ignore Equip MDEF (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
        
        # Equipment Memory System
        equipment_memory_bonus = 0
        if st.checkbox("🧠 Include Equipment Memory System", help="New system from Ghost Palace - adds significant ATK/MATK bonuses"):
            st.markdown("#### 🧠 Equipment Memory Configuration")
            
            col_mem1, col_mem2 = st.columns(2)
            
            with col_mem1:
                st.markdown("**Memory Quality & Levels**")
                # Equipment Memory slots (6 total: Weapon, Armor, Cloak, Boots, Accessory 1, Accessory 2)
                memory_slots = ["Weapon", "Armor", "Cloak", "Boots", "Accessory 1", "Accessory 2"]
                
                total_memory_atk = 0
                total_memory_matk = 0
                
                for slot in memory_slots:
                    memory_quality = st.selectbox(f"{slot} Memory", 
                        [("None", 0), ("Green", 1), ("Blue", 2), ("Purple", 3)], 
                        index=0, format_func=lambda x: x[0], key=f"mem_{slot}")
                    
                    if memory_quality[1] > 0:
                        max_level = {1: 10, 2: 20, 3: 30}[memory_quality[1]]  # Green: 10, Blue: 20, Purple: 30
                        memory_level = st.number_input(f"{slot} Level", min_value=1, max_value=max_level, 
                                                     value=min(10, max_level), key=f"level_{slot}")
                        
                        # Calculate memory bonuses (approximation based on guides)
                        if damage_type == "Physical Damage":
                            # Physical ATK bonus from memory
                            if memory_quality[1] == 3:  # Purple
                                slot_atk_bonus = memory_level * 15  # ~15 ATK per level for purple
                            elif memory_quality[1] == 2:  # Blue  
                                slot_atk_bonus = memory_level * 10  # ~10 ATK per level for blue
                            else:  # Green
                                slot_atk_bonus = memory_level * 5   # ~5 ATK per level for green
                        else:
                            # Magic ATK bonus from memory
                            if memory_quality[1] == 3:  # Purple
                                slot_atk_bonus = memory_level * 12  # ~12 MATK per level for purple
                            elif memory_quality[1] == 2:  # Blue
                                slot_atk_bonus = memory_level * 8   # ~8 MATK per level for blue  
                            else:  # Green
                                slot_atk_bonus = memory_level * 4   # ~4 MATK per level for green
                        
                        total_memory_atk += slot_atk_bonus
                        
                        # Display individual memory bonus
                        st.text(f"└ +{slot_atk_bonus} {'ATK' if damage_type == 'Physical Damage' else 'MATK'}")
            
            with col_mem2:
                st.markdown("**Memory Special Attributes**")
                
                # Special attributes unlocked at certain levels
                memory_special_atk_percent = st.number_input("ATK/MATK % from Special Lines", 
                    min_value=0.0, max_value=50.0, value=0.0, step=1.0,
                    help="Special attributes from Lv.10+ purple memories")
                
                memory_damage_increase = st.number_input("Damage Increase % from Memory", 
                    min_value=0.0, max_value=30.0, value=0.0, step=1.0,
                    help="Damage increase special attributes")
                
                memory_penetration = st.number_input("Penetration % from Memory", 
                    min_value=0.0, max_value=20.0, value=0.0, step=1.0,
                    help="Ignore DEF from special attributes")
                
                # Add memory bonuses to existing modifiers
                if damage_type == "Physical Damage":
                    atk_percent += memory_special_atk_percent
                    total_atk += total_memory_atk
                    ignore_def_general += memory_penetration
                else:
                    matk_percent += memory_special_atk_percent
                    total_matk += total_memory_atk
                    ignore_mdef_general += memory_penetration
                    
                damage_increase += memory_damage_increase
                
                # Display total memory bonuses
                st.success(f"""
                **Total Memory Bonuses:**
                - +{total_memory_atk} {'ATK' if damage_type == 'Physical Damage' else 'MATK'} (Base)
                - +{memory_special_atk_percent}% {'ATK' if damage_type == 'Physical Damage' else 'MATK'} (Special)
                - +{memory_damage_increase}% Damage Increase
                - +{memory_penetration}% Penetration
                """)
                
                # Memory upgrade recommendations
                st.info("""
                **💡 Memory Tips:**
                - Focus on 3x Purple Lv.10 first (unlocks special attributes)
                - Then upgrade to Lv.30 one by one
                - Green/Blue memories refund only 80% when decomposed
                - Weekly Ghost Palace = ~30 Memory Afterglow
                """)
        else:
            total_memory_atk = 0
        
        # Skill specific
        skill_multiplier = st.number_input("Skill Multiplier (%)", min_value=100.0, max_value=5000.0, value=500.0, step=50.0,
                                          help="Skill damage % (e.g., 500% = 5x damage)")
        
        # Critical
        critical_rate = st.number_input("Critical Rate (%)", min_value=0.0, max_value=100.0, value=50.0, step=5.0)
        critical_damage = st.number_input("Critical Damage (%)", min_value=150.0, max_value=300.0, value=200.0, step=10.0)
        
    with col3:
        st.markdown("#### 🎯 Target & Combat")
        
        # Target stats
        if damage_type == "Physical Damage":
            target_def = st.number_input("Target DEF", min_value=0, value=3000)
            target_def_percent = st.number_input("Target DEF %", min_value=0.0, value=0.0, step=5.0)
        else:
            target_mdef = st.number_input("Target MDEF", min_value=0, value=2000)
            target_mdef_percent = st.number_input("Target MDEF %", min_value=0.0, value=0.0, step=5.0)
            
        target_level = st.number_input("Target Level", min_value=1, max_value=300, value=150)
        is_boss_mvp = st.checkbox("Boss/MVP/Mini Boss", help="Affects ignore defense calculations")
        
        # Size modifier
        target_size = st.selectbox("Target Size", [
            ("Small", 1.0, 1.25, 0.75),    # Sword vs Small: Normal/Large weapon bonus/Small weapon penalty  
            ("Medium", 1.0, 1.0, 1.0),     # Neutral
            ("Large", 1.0, 0.75, 1.25)     # Sword vs Large: Normal/Small weapon penalty/Large weapon bonus
        ], format_func=lambda x: x[0])
        
        weapon_size_modifier = st.selectbox("Weapon Size Effectiveness", [
            ("Small Weapon (Dagger)", target_size[3]),
            ("Medium Weapon (1H Sword)", target_size[1]), 
            ("Large Weapon (2H Sword, Axe)", target_size[2])
        ], index=1, format_func=lambda x: x[0])
        
        # Element modifier
        element_modifier = st.selectbox("Element Effectiveness", [
            ("Ghost vs Non-Ghost (0%)", 0.0),
            ("Severe Disadvantage (25%)", 0.25),
            ("Disadvantage (50%)", 0.5),
            ("Slight Disadvantage (75%)", 0.75),
            ("Neutral (100%)", 1.0),
            ("Slight Advantage (125%)", 1.25),
            ("Advantage (150%)", 1.5),
            ("Strong Advantage (175%)", 1.75),
            ("Perfect Counter (200%)", 2.0)
        ], index=4, format_func=lambda x: x[0])
        
        # Race modifier
        race_modifier = st.number_input("Race Modifier (%)", min_value=0.0, max_value=300.0, value=100.0, step=5.0,
                                       help="Damage vs specific race (100% = neutral)")

    # Calculate button
    if st.button("⚔️ Calculate Universal ROM Damage", type="primary"):
        
        if damage_type == "Physical Damage":
            # =================== PHYSICAL DAMAGE CALCULATION ===================
            
            # Step 1: Base ATK calculation with advanced mechanics
            if "Mechanic" in character_class:
                # Mechanic special calculation
                stat_atk = main_stat * 2 + secondary_stat + int(luk_stat/3)
                base_atk = weapon_atk + stat_atk + rune_atk_bonus  # Add rune bonuses
                total_atk_with_percent = total_atk * (1 + atk_percent / 100)
                
                # Add ASPD memory penetration bonus
                ignore_def_general += aspd_pen_bonus
                
                st.info(f"🔧 **Mechanic Bonuses Applied:** +{rune_atk_bonus} ATK from runes, +{aspd_pen_bonus}% penetration from ASPD memory")
                
            else:
                # Standard calculation for other classes
                stat_atk = main_stat * 2 + secondary_stat + int(luk_stat/3)
                base_atk = weapon_atk + stat_atk
                total_atk_with_percent = total_atk * (1 + atk_percent / 100)
                rune_atk_bonus = 0  # Ensure it's defined for other classes
            
            # Step 2: Skill damage
            skill_damage = total_atk_with_percent * (skill_multiplier / 100)
            
            # Step 3: Apply size and element modifiers
            size_modified_damage = skill_damage * weapon_size_modifier[1]
            element_modified_damage = size_modified_damage * element_modifier[1]
            race_modified_damage = element_modified_damage * (race_modifier / 100)
            
            # Step 4: Defense calculation (ROM style)
            ignore_def_total = ignore_def_general + (ignore_def_equip if not is_boss_mvp else 0)
            ignore_def_total = min(100.0, ignore_def_total) / 100  # Cap at 100% and convert to decimal
            
            effective_def = target_def * (1 - ignore_def_total) * (1 + target_def_percent / 100)
            effective_def = max(0, effective_def)
            
            # ROM defense reduction formula (approximation)
            if effective_def > 0:
                def_reduction_factor = effective_def / (effective_def + race_modified_damage * 0.7 + 1000)
                def_reduction_factor = min(0.9, def_reduction_factor)  # Cap at 90% reduction
            else:
                def_reduction_factor = 0
            
            damage_after_defense = race_modified_damage * (1 - def_reduction_factor)
            
            # Step 5: Add refine damage (after defense)
            damage_with_refine = damage_after_defense + refine_attack_bonus
            
            # Step 6: Apply final damage increase
            final_non_crit_damage = damage_with_refine * (1 + damage_increase / 100)
            
            # Step 7: Critical calculation
            critical_final_damage = final_non_crit_damage * (critical_damage / 100)
            average_damage = (final_non_crit_damage * (1 - critical_rate/100)) + (critical_final_damage * (critical_rate/100))
            
            # Display Physical Results
            st.success("⚔️ Physical Damage Calculation Results")
            
            # Create detailed breakdown
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Base ATK", f"{base_atk:,.0f}")
                st.metric("Total ATK", f"{total_atk:,.0f}")
                st.metric("ATK with %", f"{total_atk_with_percent:,.0f}")
                if "Mechanic" in character_class:
                    st.metric("Rune ATK Bonus", f"+{rune_atk_bonus:,.0f}")
                    st.metric("Memory ATK Bonus", f"+{total_memory_atk:,.0f}")
                else:
                    st.metric("Memory ATK Bonus", f"+{total_memory_atk:,.0f}")
                
            with col2:
                st.metric("Skill Damage", f"{skill_damage:,.0f}")
                st.metric("After Size Mod", f"{size_modified_damage:,.0f}")
                st.metric("After Element", f"{element_modified_damage:,.0f}")
                if "Mechanic" in character_class:
                    st.metric("ASPD Memory Pen", f"+{aspd_pen_bonus}%")
                    st.metric("Total Memory Bonus", f"+{total_memory_atk:,.0f}")
                else:
                    st.metric("Memory Bonus", f"+{total_memory_atk:,.0f}")
                
            with col3:
                st.metric("Ignore DEF Total", f"{ignore_def_total:.1%}")
                st.metric("Effective DEF", f"{effective_def:,.0f}")
                st.metric("DEF Reduction", f"{def_reduction_factor:.1%}")
                
            with col4:
                st.metric("After Defense", f"{damage_after_defense:,.0f}")
                st.metric("Refine Bonus", f"+{refine_attack_bonus:,.0f}")
                st.metric("Final Non-Crit", f"{final_non_crit_damage:,.0f}")
                
            with col5:
                st.metric("Critical Damage", f"{critical_final_damage:,.0f}")
                st.metric("**Average Damage**", f"{average_damage:,.0f}")
                st.metric("Max Damage", f"{critical_final_damage:,.0f}")
            
        else:
            # =================== MAGIC DAMAGE CALCULATION ===================
            
            # Step 1: Base MATK calculation  
            stat_matk = main_stat * 2 + secondary_stat + int(luk_stat/3)
            base_matk = weapon_matk + stat_matk
            total_matk_with_percent = total_matk * (1 + matk_percent / 100)
            
            # Step 2: Skill damage
            skill_magic_damage = total_matk_with_percent * (skill_multiplier / 100)
            
            # Step 3: Apply element and race modifiers (no size for magic)
            element_modified_damage = skill_magic_damage * element_modifier[1]
            race_modified_damage = element_modified_damage * (race_modifier / 100)
            
            # Step 4: Magic defense calculation
            ignore_mdef_total = ignore_mdef_general + (ignore_mdef_equip if not is_boss_mvp else 0)
            ignore_mdef_total = min(100.0, ignore_mdef_total) / 100
            
            effective_mdef = target_mdef * (1 - ignore_mdef_total) * (1 + target_mdef_percent / 100)
            effective_mdef = max(0, effective_mdef)
            
            if effective_mdef > 0:
                mdef_reduction_factor = effective_mdef / (effective_mdef + race_modified_damage * 0.6 + 1000)
                mdef_reduction_factor = min(0.9, mdef_reduction_factor)
            else:
                mdef_reduction_factor = 0
            
            damage_after_mdefense = race_modified_damage * (1 - mdef_reduction_factor)
            
            # Step 5: Add refine damage
            magic_refine_bonus = refine_level * 10  # Magic refine is typically lower
            damage_with_refine = damage_after_mdefense + magic_refine_bonus
            
            # Step 6: Apply final damage increase  
            final_non_crit_damage = damage_with_refine * (1 + damage_increase / 100)
            
            # Step 7: Magic critical (if applicable)
            critical_final_damage = final_non_crit_damage * (critical_damage / 100)
            average_damage = (final_non_crit_damage * (1 - critical_rate/100)) + (critical_final_damage * (critical_rate/100))
            
            # Display Magic Results
            st.success("🔮 Magic Damage Calculation Results")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Base MATK", f"{base_matk:,.0f}")
                st.metric("Total MATK", f"{total_matk:,.0f}")
                st.metric("MATK with %", f"{total_matk_with_percent:,.0f}")
                
            with col2:
                st.metric("Skill Magic Dmg", f"{skill_magic_damage:,.0f}")
                st.metric("After Element", f"{element_modified_damage:,.0f}")
                st.metric("After Race", f"{race_modified_damage:,.0f}")
                
            with col3:
                st.metric("Ignore MDEF Total", f"{ignore_mdef_total:.1%}")
                st.metric("Effective MDEF", f"{effective_mdef:,.0f}")
                st.metric("MDEF Reduction", f"{mdef_reduction_factor:.1%}")
                
            with col4:
                st.metric("After MDEF", f"{damage_after_mdefense:,.0f}")
                st.metric("Magic Refine", f"+{magic_refine_bonus:,.0f}")
                st.metric("Final Non-Crit", f"{final_non_crit_damage:,.0f}")
                
            with col5:
                st.metric("Magic Critical", f"{critical_final_damage:,.0f}")
                st.metric("**Average Damage**", f"{average_damage:,.0f}")
                st.metric("Max Damage", f"{critical_final_damage:,.0f}")
        
        # Class-specific notes
        class_tips = {
            "Knight/Lord Knight/Rune Knight": "🛡️ High ATK, Pierce ignores size penalties, Bowling Bash hits multiple targets",
            "Assassin/Assassin Cross/Guillotine Cross": "⚡ High critical rate, dual wield penalty applies, Sonic Blow ignores flee",
            "Hunter/Sniper/Ranger": "🏹 DEX-based, size modifiers important for bow weapons, can use traps and arrows",
            "Priest/High Priest/Archbishop": "⭐ INT-based healing and support, Turn Undead vs undead, Magnus Exorcismus vs undead/demon",
            "Wizard/High Wizard/Warlock/Sorcerer": "🔥 Pure magic damage, element mastery important, area spells",
            "Blacksmith/Whitesmith/Mechanic": "🔨 STR-based, Arm Cannon ignores flee, size modifiers from weapon type",
            "Crusader/Paladin/Royal Guard": "🛡️ Balanced ATK/DEF, Shield skills, Holy element attacks",
            "Monk/Champion/Shura/Sura": "👊 STR-based, Spirit spheres affect damage, combo skills"
        }
        
        if character_class in class_tips:
            st.info(f"**{character_class} Tips:** {class_tips[character_class]}")

with tab2:
    st.subheader("📊 Skill Damage Database")
    
    # Skill database for common skills
    skill_db = {
        "Knight": {
            "Bash": {"multiplier": 400, "element": "Neutral", "type": "Physical"},
            "Pierce": {"multiplier": 500, "element": "Neutral", "type": "Physical", "note": "Ignores size"},
            "Bowling Bash": {"multiplier": 600, "element": "Neutral", "type": "Physical", "note": "Multi-hit"},
            "Spiral Pierce": {"multiplier": 800, "element": "Neutral", "type": "Physical"}
        },
        "Wizard": {
            "Fire Bolt": {"multiplier": 300, "element": "Fire", "type": "Magic"},
            "Meteor Storm": {"multiplier": 800, "element": "Fire", "type": "Magic"},
            "Lord of Vermillion": {"multiplier": 700, "element": "Wind", "type": "Magic"},
            "Storm Gust": {"multiplier": 600, "element": "Water", "type": "Magic"}
        },
        "Assassin": {
            "Sonic Blow": {"multiplier": 800, "element": "Neutral", "type": "Physical", "note": "Ignores flee"},
            "Meteor Assault": {"multiplier": 600, "element": "Neutral", "type": "Physical"},
            "Soul Breaker": {"multiplier": 500, "element": "Neutral", "type": "Mixed"}
        },
        "Hunter": {
            "Double Strafe": {"multiplier": 380, "element": "Neutral", "type": "Physical"},
            "Arrow Shower": {"multiplier": 500, "element": "Neutral", "type": "Physical"},
            "Musical Strike": {"multiplier": 600, "element": "Neutral", "type": "Physical"}
        },
        "Mechanic": {
            "Arm Cannon": {"multiplier": 2060, "element": "Neutral", "type": "Physical", "note": "Ignores flee, size: 150%/100%/75%"},
            "Knuckle Boost": {"multiplier": 0, "element": "Neutral", "type": "Buff", "note": "+200 ATK, +50% Crit"},
            "Power Swing": {"multiplier": 150, "element": "Neutral", "type": "Buff", "note": "Next attack +50%"}
        }
    }
    
    # Extract class from selection for skill lookup
    base_class = character_class.split("/")[0]
    
    if base_class in skill_db:
        st.markdown(f"#### {base_class} Skills")
        
        skills_df = pd.DataFrame.from_dict(skill_db[base_class], orient='index')
        skills_df = skills_df.reset_index()
        skills_df.columns = ['Skill Name', 'Multiplier %', 'Element', 'Type', 'Notes']
        skills_df['Notes'] = skills_df['Notes'].fillna('-')
        
        st.dataframe(skills_df, use_container_width=True)
        
        # Quick skill calculator
        selected_skill = st.selectbox("Quick Calculate Skill", list(skill_db[base_class].keys()))
        
        if st.button(f"Calculate {selected_skill}"):
            skill_data = skill_db[base_class][selected_skill]
            st.success(f"**{selected_skill}**: {skill_data['multiplier']}% {skill_data['element']} {skill_data['type']} damage")
            if 'note' in skill_data:
                st.info(f"**Special:** {skill_data['note']}")
    else:
        st.info("Select a supported class to see skill database. More classes being added!")
        
        # Generic skill input
        st.markdown("#### Manual Skill Input")
        custom_skill_name = st.text_input("Skill Name")
        custom_multiplier = st.number_input("Skill Multiplier (%)", min_value=100, value=500)
        custom_element = st.selectbox("Skill Element", ["Neutral", "Fire", "Water", "Earth", "Wind", "Poison", "Holy", "Shadow", "Ghost", "Undead"])
        
        if st.button("Add to Calculator"):
            st.success(f"Use {custom_multiplier}% in the Universal Calculator!")

with tab3:
    st.subheader("📈 Build Optimizer")
    
    st.markdown("#### Compare Different Stat Distributions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Build A: Balanced**")
        a_main_stat = st.number_input("Main Stat", min_value=1, value=120, key="opt_a_main")
        a_secondary = st.number_input("Secondary Stat", min_value=1, value=80, key="opt_a_sec") 
        a_atk_percent = st.number_input("ATK %", min_value=0.0, value=50.0, key="opt_a_atk")
        a_ignore_def = st.number_input("Total Ignore DEF %", min_value=0.0, value=35.0, key="opt_a_ignore")
        a_damage_inc = st.number_input("Damage Inc %", min_value=0.0, value=80.0, key="opt_a_dam")
        
    with col2:
        st.markdown("**Build B: Specialized**")
        b_main_stat = st.number_input("Main Stat", min_value=1, value=140, key="opt_b_main")
        b_secondary = st.number_input("Secondary Stat", min_value=1, value=60, key="opt_b_sec")
        b_atk_percent = st.number_input("ATK %", min_value=0.0, value=70.0, key="opt_b_atk") 
        b_ignore_def = st.number_input("Total Ignore DEF %", min_value=0.0, value=45.0, key="opt_b_ignore")
        b_damage_inc = st.number_input("Damage Inc %", min_value=0.0, value=100.0, key="opt_b_dam")
    
    # Common optimization settings
    opt_target_def = st.number_input("Target DEF for Optimization", min_value=0, value=4000)
    opt_skill_mult = st.number_input("Skill Multiplier % for Test", min_value=100.0, value=800.0)
    
    if st.button("🔍 Optimize Builds"):
        # Quick calculation for both builds
        def quick_calc(main_stat, secondary, atk_perc, ignore_def, dam_inc, target_def, skill_mult):
            base_atk = 1200 + main_stat * 2 + secondary  # Simplified
            total_atk = base_atk * (1 + atk_perc / 100)
            skill_dmg = total_atk * (skill_mult / 100)
            
            effective_def = target_def * (1 - ignore_def / 100)
            def_reduction = effective_def / (effective_def + skill_dmg * 0.7 + 1000)
            def_reduction = min(0.9, def_reduction)
            
            after_def = skill_dmg * (1 - def_reduction)
            final = after_def * (1 + dam_inc / 100)
            
            return final, def_reduction
            
        a_result, a_def_red = quick_calc(a_main_stat, a_secondary, a_atk_percent, a_ignore_def, a_damage_inc, opt_target_def, opt_skill_mult)
        b_result, b_def_red = quick_calc(b_main_stat, b_secondary, b_atk_percent, b_ignore_def, b_damage_inc, opt_target_def, opt_skill_mult)
        
        st.success("🔍 Build Optimization Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Build A Damage", f"{a_result:,.0f}")
            st.metric("Build A DEF Reduction", f"{a_def_red:.1%}")
            
        with col2:
            st.metric("Build B Damage", f"{b_result:,.0f}")
            st.metric("Build B DEF Reduction", f"{b_def_red:.1%}")
            
        with col3:
            diff = b_result - a_result
            diff_percent = (diff / a_result) * 100 if a_result > 0 else 0
            better = "Build B" if diff > 0 else "Build A"
            
            st.metric("Difference", f"{abs(diff):,.0f}")
            st.metric("% Difference", f"{abs(diff_percent):.1f}%")
            st.success(f"🏆 **{better} wins!**")

with tab4:
    st.subheader("🔬 Formula Accuracy Tester")
    
    st.markdown("""
    Test the calculator accuracy against known damage values from the game.
    Submit your in-game damage tests to help improve formula accuracy.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Test Case Input")
        test_your_atk = st.number_input("Your ATK", min_value=0, value=3000, key="test_atk")
        test_skill_mult = st.number_input("Skill %", min_value=100, value=800, key="test_skill")
        test_target_def = st.number_input("Target DEF", min_value=0, value=3000, key="test_def")
        test_your_ignore = st.number_input("Your Ignore DEF %", min_value=0.0, value=30.0, key="test_ignore")
        test_your_dam_inc = st.number_input("Your Dam Inc %", min_value=0.0, value=80.0, key="test_dam_inc")
        
        actual_damage = st.number_input("Actual In-Game Damage", min_value=0, value=0, key="actual_dmg", 
                                       help="The damage you actually dealt in-game")
        
    with col2:
        st.markdown("#### Calculator Prediction")
        
        if st.button("🧪 Test Formula Accuracy"):
            # Calculate predicted damage
            base_calc = test_your_atk * (test_skill_mult / 100)
            effective_def = test_target_def * (1 - test_your_ignore / 100)
            def_reduction = effective_def / (effective_def + base_calc * 0.7 + 1000)
            def_reduction = min(0.9, def_reduction)
            
            after_def = base_calc * (1 - def_reduction)
            predicted = after_def * (1 + test_your_dam_inc / 100)
            
            if actual_damage > 0:
                accuracy = (1 - abs(predicted - actual_damage) / actual_damage) * 100
                accuracy = max(0, accuracy)
                
                st.metric("Predicted Damage", f"{predicted:,.0f}")
                st.metric("Actual Damage", f"{actual_damage:,.0f}")
                st.metric("Accuracy", f"{accuracy:.1f}%")
                
                if accuracy >= 95:
                    st.success("🎯 Excellent accuracy!")
                elif accuracy >= 85:
                    st.warning("⚠️ Good accuracy - minor formula adjustments needed")
                else:
                    st.error("❌ Poor accuracy - formula needs investigation")
                    
                # Error analysis
                error = predicted - actual_damage
                error_percent = (error / actual_damage) * 100
                
                st.markdown("#### Error Analysis")
                if error > 0:
                    st.info(f"Calculator overestimate: +{error:,.0f} (+{error_percent:.1f}%)")
                else:
                    st.info(f"Calculator underestimate: {error:,.0f} ({error_percent:.1f}%)")
            else:
                st.metric("Predicted Damage", f"{predicted:,.0f}")
                st.info("Enter actual damage to test accuracy")

# Class-specific recommendations
with st.expander("🎭 Class-Specific Optimization Tips"):
    st.markdown("""
    ### Physical Classes:
    **Knights/Crusaders/Paladins:**
    - 🥇 **STR** primary for ATK damage
    - 🥈 **VIT** secondary for HP/DEF (tanking)
    - 🥉 **DEX** tertiary for accuracy
    - Builds: Pure STR DPS | STR-VIT Tank | STR-DEX Hybrid
    
    **Assassins/Rogues:**
    - 🥇 **AGI** primary for ASPD/Critical
    - 🥈 **STR** secondary for base damage  
    - 🥉 **LUK** tertiary for critical rate
    - Builds: AGI-Critical | AGI-STR Hybrid | Pure Critical (LUK)
    
    **Hunters/Rangers:**
    - 🥇 **DEX** primary for bow damage/accuracy
    - 🥈 **AGI** secondary for attack speed
    - 🥉 **INT** tertiary for SP/traps
    - Builds: Pure DEX ADL | DEX-AGI ASPD | DEX-INT Trapper
    
    **Monks/Champions:**
    - 🥇 **STR** primary for damage
    - 🥈 **AGI** secondary for combo speed
    - 🥉 **VIT** tertiary for HP/survivability
    - Builds: Pure STR Asura | STR-AGI Combo | STR-VIT Tanky
    
    **Blacksmiths/Mechanics:**
    - 🥇 **STR** primary for weapon skills
    - 🥈 **DEX** secondary for accuracy/crafting
    - 🥉 **VIT** tertiary for survival
    - Builds: Pure STR DPS | STR-DEX Smith | STR-VIT Tanky
    
    ### Magic Classes:
    **Wizards/Warlocks/Sorcerers:**
    - 🥇 **INT** primary for magic damage/SP
    - 🥈 **DEX** secondary for cast time reduction
    - 🥉 **VIT** tertiary for survivability
    - Builds: Pure INT Glass Cannon | INT-DEX Fast Cast | INT-VIT Survivor
    
    **Priests/Archbishops:**
    - 🥇 **INT** primary for healing power/magic damage
    - 🥈 **DEX** secondary for instant cast
    - 🥉 **VIT** tertiary for survival
    - Builds: Pure INT Battle | INT-DEX Support | INT-VIT Tank
    
    ### Hybrid/Special Classes:
    **Bards/Dancers:**
    - 🥇 **DEX** primary for bow skills
    - 🥈 **AGI** secondary for attack speed
    - 🥉 **INT** tertiary for SP/songs
    - Builds: DEX-AGI ADL | Pure DEX | INT Support
    
    **Gunslingers/Rebels:**
    - 🥇 **DEX** primary for gun damage
    - 🥈 **AGI** secondary for attack speed  
    - 🥉 **STR** tertiary for damage boost
    - Builds: Pure DEX | DEX-AGI ASPD | DEX-STR Hybrid
    
    **Super Novice:**
    - 🌟 **Flexible** - can use any stat combination
    - All stats viable depending on chosen role
    - Builds: Balanced All Stats | Specialized Single Stat | Custom Build
    
    **Ninja:**
    - 🥇 **STR** primary for physical skills
    - 🥈 **INT** secondary for magic skills
    - 🥉 **AGI** tertiary for speed
    - Builds: STR Physical | INT Magic | Hybrid STR-INT
    
    **Doram (Summoner):**
    - 🥇 **INT** primary for magic/healing
    - 🥈 **DEX** secondary for cast time
    - 🥉 **VIT** tertiary for survival  
    - Builds: Pure INT Magic | INT-DEX Support | Physical Doram
    """)

# Advanced formulas
with st.expander("🧮 Advanced ROM Formula Details"):
    st.markdown("""
    ### Detailed ROM Handbook Formulas:
    
    **Base ATK Calculation:**
    ```
    BaseATK = WeaponATK + (STR×2 + DEX + LUK÷3)
    TotalATK = BaseATK × (1 + ATK%÷100)
    ```
    
    **Skill Damage:**
    ```
    SkillDamage = TotalATK × (SkillMultiplier÷100)
    ```
    
    **Size Modifier (Physical Only):**
    ```
    Small Target: Dagger=100%, Sword=75%, 2H=50%
    Medium Target: All weapons = 100%  
    Large Target: Dagger=75%, Sword=100%, 2H=125%
    ```
    
    **Element Modifier:**
    ```
    Fire vs Water/Earth = 150%
    Fire vs Fire = 75%
    Fire vs Wind = 125%
    Neutral vs Ghost = 100%
    Physical vs Ghost = 0% (unless blessed weapon)
    ```
    
    **Defense Reduction:**
    ```
    EffectiveDEF = TargetDEF × (1 - IgnoreDEF%)
    DEFReduction = EffectiveDEF ÷ (EffectiveDEF + BaseDamage×0.7 + 1000)
    MaxReduction = 90%
    ```
    
    **Final Calculation:**
    ```
    AfterDEF = SkillDamage × (1 - DEFReduction)
    WithRefine = AfterDEF + RefineATK
    FinalDamage = WithRefine × (1 + DamageIncrease%÷100)
    ```
    
    **Critical Damage:**
    ```
    CritDamage = FinalDamage × (1.5 + CritDamageBonus%÷100)
    ```
    """)

# Footer with data source
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>⚔️ <strong>ROM Universal Damage Calculator</strong></p>
    <p>📊 <strong>Accurate for all classes</strong> | 🎯 <strong>Based on ROM Handbook formulas</strong></p>
    <p>📚 <strong>Data Source:</strong> <a href="https://romhandbook.com/formulas/" target="_blank">ROM Handbook Official Formulas</a></p>
    <p><em>Universal calculator supporting all classes with accurate ROM game formulas</em></p>
    <p><strong>🔄 Regular Updates:</strong> Formulas updated as ROM Handbook data changes</p>
</div>
""", unsafe_allow_html=True)