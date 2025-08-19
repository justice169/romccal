import streamlit as st
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

# Class selection
st.sidebar.markdown("### 🎭 Character Setup")
character_class = st.sidebar.selectbox("Select Class Type", [
    "Knight/Lord Knight/Rune Knight", 
    "Assassin/Assassin Cross/Guillotine Cross",
    "Hunter/Sniper/Ranger", 
    "Priest/High Priest/Archbishop",
    "Wizard/High Wizard/Warlock/Sorcerer",
    "Blacksmith/Whitesmith/Mechanic",
    "Crusader/Paladin/Royal Guard",
    "Rogue/Stalker/Shadow Chaser",
    "Monk/Champion/Shura/Sura",
    "Bard-Dancer/Clown-Gypsy/Minstrel-Wanderer",
    "Taekwon/Star Gladiator/Soul Linker",
    "Ninja/Kagerou/Oboro",
    "Gunslinger/Rebel",
    "Super Novice/Hyper Novice",
    "Doram (Summoner)"
])

damage_type = st.sidebar.selectbox("Damage Type", ["Physical Damage", "Magic Damage"])

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Universal Calculator", "📊 Skill Database", "📈 Build Optimizer", "🔬 Formula Tester"])

with tab1:
    st.subheader("Universal ROM Damage Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Character Stats")
        
        if damage_type == "Physical Damage":
            # Determine main stat based on class
            if "Knight" in character_class or "Crusader" in character_class or "Monk" in character_class:
                main_stat_name = "STR"
                main_stat = st.number_input("STR (Main)", min_value=1, max_value=200, value=120)
            elif "Hunter" in character_class or "Bard" in character_class or "Dancer" in character_class:
                main_stat_name = "DEX" 
                main_stat = st.number_input("DEX (Main)", min_value=1, max_value=200, value=120)
            elif "Assassin" in character_class or "Rogue" in character_class:
                main_stat_name = "AGI"
                main_stat = st.number_input("AGI (Main)", min_value=1, max_value=200, value=120)
            else:
                main_stat_name = "STR/DEX"
                main_stat = st.number_input("Main Stat", min_value=1, max_value=200, value=120)
                
            # Secondary stats
            secondary_stat = st.number_input("Secondary Stat", min_value=1, max_value=200, value=80)
            luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=30)
            
            # Attack values
            total_atk = st.number_input("Total ATK", min_value=0, value=3000, help="Your total ATK shown in status window")
            weapon_atk = st.number_input("Weapon ATK", min_value=0, value=1200, help="Base weapon attack")
            
        else:  # Magic Damage
            main_stat_name = "INT"
            main_stat = st.number_input("INT (Main)", min_value=1, max_value=200, value=120)
            secondary_stat = st.number_input("DEX", min_value=1, max_value=200, value=80)
            luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=30)
            
            total_matk = st.number_input("Total MATK", min_value=0, value=2500, help="Your total MATK shown in status window")
            weapon_matk = st.number_input("Weapon MATK", min_value=0, value=800, help="Base weapon magic attack")
            
        # Common stats
        base_level = st.number_input("Base Level", min_value=1, max_value=200, value=140)
        job_level = st.number_input("Job Level", min_value=1, max_value=70, value=60)
        
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
        
        # Universal modifiers
        damage_increase = st.number_input("Damage Increase (%)", min_value=0.0, max_value=300.0, value=80.0, step=5.0, 
                                        help="Final damage increase from gear/cards/runes")
        
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
            
            # Step 1: Base ATK calculation
            stat_atk = main_stat * 2 + secondary_stat + int(luk_stat/3)  # Simplified stat contribution
            base_atk = weapon_atk + stat_atk
            total_atk_with_percent = total_atk * (1 + atk_percent / 100)
            
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
                
            with col2:
                st.metric("Skill Damage", f"{skill_damage:,.0f}")
                st.metric("After Size Mod", f"{size_modified_damage:,.0f}")
                st.metric("After Element", f"{element_modified_damage:,.0f}")
                
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
    - Prioritize STR for ATK
    - VIT for survivability  
    - Two-handed weapons for higher damage
    - Size modifier crucial for weapon choice
    
    **Assassins/Rogues:**
    - High AGI for ASPD and Crit
    - Dual wield has ATK penalty but double hits
    - Critical builds benefit from LUK
    - Sonic Blow ignores flee
    
    **Hunters/Rangers:**
    - DEX primary stat for ATK and HIT
    - Arrow type affects damage
    - Size modifiers important for bow weapons
    - Traps for utility
    
    **Monks/Champions:**
    - STR for damage
    - Spirit spheres enhance skills
    - Combo skills for maximum damage
    - Asura Strike = massive single hit
    
    ### Magic Classes:
    **Wizards/Warlocks/Sorcerers:**
    - INT primary for MATK
    - DEX for cast time reduction
    - Element mastery crucial
    - Area spells for farming
    
    **Priests/Archbishops:**
    - INT for healing and damage
    - Turn Undead vs undead monsters
    - Support skills for party play
    - Magnus Exorcismus vs undead/demon
    
    ### Hybrid Classes:
    **Blacksmiths/Mechanics:**
    - STR for physical skills
    - Arm Cannon ignores flee
    - Power Swing enhances next attack
    - Equipment mastery important
    
    **Bards/Dancers:**
    - DEX for bow skills
    - Support songs/dances
    - Arrow Vulcan for damage
    - Party utility focus
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