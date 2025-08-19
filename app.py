import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Ragnarok M Damage Calculator",
    page_icon="⚔️",
    layout="wide"
)

# Title and description
st.title("⚔️ Ragnarok M: Eternal Love Damage Calculator")
st.markdown("""
Calculate your character's damage output based on the official damage formulas.
Supports both Physical and Magic damage calculations.
""")

# Damage formula display
with st.expander("📋 Damage Formula Reference"):
    st.markdown("""
    **Physical Damage Formula:**
    ```
    (((baseAtk + MainStat*3 + bonusAA) * AtkInc% * WeaponSize * SizeMod * ElementMod * ConverterMod * ElementDmgInc + StatsAtk) 
    * RaceMod * Penetration * HiddenRefineBonus * DefRed) + RefineAtk) * GearSkillMod * RuneMod * SkillMod% * DmgInc%
    ```
    
    **Magic Damage Formula:**
    ```
    (((baseMAtk + INT*2 + bonusMA) * MAtkInc% * ElementMod * ConverterMod * ElementDmgInc + StatsMAtk) 
    * RaceMod * MPenetration * HiddenRefineBonus * MDefRed) + RefineMAtk) * GearSkillMod * RuneMod * SkillMod% * DmgInc%
    ```
    
    **Priority Order:** DmgInc > Penetration > Crit% > Skill% = Runes% > Race > Size = Element = Converter = Atk%
    """)

# Sidebar for damage type selection
damage_type = st.sidebar.selectbox("🎯 Select Damage Type", ["Physical Damage", "Magic Damage"])

# Create tabs
tab1, tab2, tab3 = st.tabs(["📊 Basic Calculator", "🔧 Advanced Calculator", "📈 Comparison Tool"])

with tab1:
    st.subheader("Basic Damage Calculator")
    
    if damage_type == "Physical Damage":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Character Stats")
            base_level = st.number_input("Base Level", min_value=1, max_value=200, value=100)
            job_level = st.number_input("Job Level", min_value=1, max_value=90, value=40)
            
            # Main stats
            str_stat = st.number_input("STR", min_value=1, max_value=500, value=100)
            agi_stat = st.number_input("AGI", min_value=1, max_value=500, value=50)
            vit_stat = st.number_input("VIT", min_value=1, max_value=500, value=50)
            dex_stat = st.number_input("DEX", min_value=1, max_value=500, value=50)
            
            # Basic attack values
            weapon_atk = st.number_input("Weapon Attack", min_value=0, value=1000)
            refine_level = st.number_input("Refine Level (+)", min_value=0, max_value=15, value=0)
            
        with col2:
            st.markdown("#### Modifiers (%)")
            atk_inc = st.number_input("Attack Increase %", min_value=0.0, max_value=1000.0, value=0.0, step=1.0)
            size_mod = st.selectbox("Size Modifier", [75, 100, 125], index=1, format_func=lambda x: f"{x}%")
            element_mod = st.selectbox("Element Modifier", [25, 50, 75, 100, 125, 150, 175, 200], index=3, format_func=lambda x: f"{x}%")
            race_mod = st.number_input("Race Modifier %", min_value=0.0, max_value=200.0, value=100.0, step=5.0)
            dmg_inc = st.number_input("Damage Increase %", min_value=0.0, max_value=500.0, value=0.0, step=1.0)
            penetration = st.number_input("Penetration %", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            
            # Target defense
            target_def = st.number_input("Target DEF", min_value=0, value=0)
            
        # Calculate physical damage
        if st.button("⚔️ Calculate Physical Damage"):
            # Base calculations
            main_stat_bonus = str_stat * 3
            base_atk = weapon_atk + main_stat_bonus
            refine_atk = refine_level * 12
            
            # Apply modifiers (convert percentages)
            atk_inc_mod = 1 + (atk_inc / 100)
            size_mod_val = size_mod / 100
            element_mod_val = element_mod / 100
            race_mod_val = race_mod / 100
            dmg_inc_mod = 1 + (dmg_inc / 100)
            pen_reduction = 1 - (penetration / 100)
            
            # Defense reduction (simplified)
            def_reduction = max(0.1, 1 - (target_def / (target_def + 4000)))
            
            # Calculate damage using simplified formula
            base_damage = base_atk * atk_inc_mod * size_mod_val * element_mod_val
            modified_damage = base_damage * race_mod_val * def_reduction * pen_reduction
            final_damage = (modified_damage + refine_atk) * dmg_inc_mod
            
            # Display results
            st.success("🎯 Damage Calculation Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Base Attack", f"{base_atk:,.0f}")
                st.metric("Refine Attack", f"{refine_atk:,.0f}")
                
            with col2:
                st.metric("Modified Damage", f"{modified_damage:,.0f}")
                st.metric("Defense Reduction", f"{def_reduction:.2%}")
                
            with col3:
                st.metric("**Final Damage**", f"{final_damage:,.0f}", delta=f"+{final_damage-base_atk:,.0f}")
                
    else:  # Magic Damage
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Character Stats")
            base_level = st.number_input("Base Level", min_value=1, max_value=200, value=100)
            job_level = st.number_input("Job Level", min_value=1, max_value=70, value=40)
            
            # Main stats for magic
            int_stat = st.number_input("INT", min_value=1, max_value=200, value=120)
            dex_stat = st.number_input("DEX", min_value=1, max_value=200, value=80)
            
            # Magic attack values
            weapon_matk = st.number_input("Weapon Magic Attack", min_value=0, value=800)
            refine_level = st.number_input("Refine Level (+)", min_value=0, max_value=15, value=0)
            
        with col2:
            st.markdown("#### Modifiers (%)")
            matk_inc = st.number_input("Magic Attack Increase %", min_value=0.0, max_value=1000.0, value=0.0, step=1.0)
            element_mod = st.selectbox("Element Modifier", [25, 50, 75, 100, 125, 150, 175, 200], index=3, format_func=lambda x: f"{x}%")
            race_mod = st.number_input("Race Modifier %", min_value=0.0, max_value=200.0, value=100.0, step=5.0)
            dmg_inc = st.number_input("Damage Increase %", min_value=0.0, max_value=500.0, value=0.0, step=1.0)
            m_penetration = st.number_input("Magic Penetration %", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            
            # Target magic defense
            target_mdef = st.number_input("Target MDEF", min_value=0, value=0)
            
        # Calculate magic damage
        if st.button("🔮 Calculate Magic Damage"):
            # Base calculations
            int_bonus = int_stat * 2
            base_matk = weapon_matk + int_bonus
            refine_matk = refine_level * 12
            
            # Apply modifiers
            matk_inc_mod = 1 + (matk_inc / 100)
            element_mod_val = element_mod / 100
            race_mod_val = race_mod / 100
            dmg_inc_mod = 1 + (dmg_inc / 100)
            mpen_reduction = 1 - (m_penetration / 100)
            
            # Magic defense reduction
            mdef_reduction = max(0.1, 1 - (target_mdef / (target_mdef + 4000)))
            
            # Calculate magic damage
            base_damage = base_matk * matk_inc_mod * element_mod_val
            modified_damage = base_damage * race_mod_val * mdef_reduction * mpen_reduction
            final_damage = (modified_damage + refine_matk) * dmg_inc_mod
            
            # Display results
            st.success("🎯 Magic Damage Calculation Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Base Magic Attack", f"{base_matk:,.0f}")
                st.metric("Refine Magic Attack", f"{refine_matk:,.0f}")
                
            with col2:
                st.metric("Modified Damage", f"{modified_damage:,.0f}")
                st.metric("MDEF Reduction", f"{mdef_reduction:.2%}")
                
            with col3:
                st.metric("**Final Magic Damage**", f"{final_damage:,.0f}", delta=f"+{final_damage-base_matk:,.0f}")

with tab2:
    st.subheader("Advanced Damage Calculator")
    st.markdown("*Advanced calculator with all modifiers including cards, runes, and skills*")
    
    if damage_type == "Physical Damage":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Base Stats")
            str_stat = st.number_input("STR", min_value=1, max_value=200, value=100, key="adv_str")
            agi_stat = st.number_input("AGI", min_value=1, max_value=200, value=50, key="adv_agi")
            vit_stat = st.number_input("VIT", min_value=1, max_value=200, value=50, key="adv_vit")
            dex_stat = st.number_input("DEX", min_value=1, max_value=200, value=50, key="adv_dex")
            int_stat = st.number_input("INT", min_value=1, max_value=200, value=20, key="adv_int")
            luk_stat = st.number_input("LUK", min_value=1, max_value=200, value=20, key="adv_luk")
            
        with col2:
            st.markdown("#### Equipment & Refine")
            weapon_atk = st.number_input("Weapon Attack", min_value=0, value=1000, key="adv_weapon")
            refine_level = st.number_input("Refine Level (+)", min_value=0, max_value=15, value=0, key="adv_refine")
            
            st.markdown("#### Cards & Enchants")
            card_atk = st.number_input("Card Attack Bonus", min_value=0, value=0, key="adv_card")
            enchant_atk = st.number_input("Enchant Attack Bonus", min_value=0, value=0, key="adv_enchant")
            
        with col3:
            st.markdown("#### Advanced Modifiers")
            atk_inc = st.number_input("Attack Increase %", min_value=0.0, max_value=1000.0, value=0.0, step=1.0, key="adv_atk_inc")
            size_mod = st.selectbox("Size Modifier", [75, 100, 125], index=1, format_func=lambda x: f"{x}%", key="adv_size")
            element_mod = st.selectbox("Element Modifier", [25, 50, 75, 100, 125, 150, 175, 200], index=3, format_func=lambda x: f"{x}%", key="adv_element")
            converter_mod = st.number_input("Converter Modifier %", min_value=0.0, max_value=200.0, value=100.0, step=5.0, key="adv_converter")
            race_mod = st.number_input("Race Modifier %", min_value=0.0, max_value=200.0, value=100.0, step=5.0, key="adv_race")
            
            st.markdown("#### Final Modifiers")
            skill_mod = st.number_input("Skill Modifier %", min_value=0.0, max_value=2000.0, value=100.0, step=10.0, key="adv_skill")
            rune_mod = st.number_input("Rune Modifier %", min_value=0.0, max_value=500.0, value=100.0, step=5.0, key="adv_rune")
            gear_skill_mod = st.number_input("Gear/Set Skill Modifier %", min_value=0.0, max_value=500.0, value=100.0, step=5.0, key="adv_gear")
            dmg_inc = st.number_input("Damage Increase %", min_value=0.0, max_value=500.0, value=0.0, step=1.0, key="adv_dmg_inc")
            penetration = st.number_input("Penetration %", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key="adv_pen")
            
        st.markdown("#### Target Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            target_def = st.number_input("Target DEF", min_value=0, value=0, key="adv_target_def")
        with col2:
            target_level = st.number_input("Target Level", min_value=1, max_value=300, value=100, key="adv_target_level")
        with col3:
            crit_chance = st.number_input("Critical Chance %", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key="adv_crit")
            
        if st.button("⚔️ Calculate Advanced Physical Damage"):
            # Base calculations
            main_stat_bonus = str_stat * 3
            base_atk = weapon_atk + main_stat_bonus + card_atk + enchant_atk
            refine_atk = refine_level * 12
            
            # Convert percentages to multipliers
            atk_inc_mod = 1 + (atk_inc / 100)
            size_mod_val = size_mod / 100
            element_mod_val = element_mod / 100
            converter_mod_val = converter_mod / 100
            race_mod_val = race_mod / 100
            skill_mod_val = skill_mod / 100
            rune_mod_val = rune_mod / 100
            gear_mod_val = gear_skill_mod / 100
            dmg_inc_mod = 1 + (dmg_inc / 100)
            
            # Penetration and defense calculations
            pen_reduction = 1 - (penetration / 100)
            def_reduction = max(0.1, 1 - (target_def / (target_def + 4000)))
            
            # Full damage formula calculation
            step1 = base_atk * atk_inc_mod * size_mod_val * element_mod_val * converter_mod_val
            step2 = step1 * race_mod_val * pen_reduction * def_reduction
            step3 = (step2 + refine_atk) * gear_mod_val * rune_mod_val * skill_mod_val * dmg_inc_mod
            
            # Critical damage calculation
            crit_damage = step3 * 1.5 if crit_chance > 0 else 0
            average_damage = step3 * (1 - crit_chance/100) + crit_damage * (crit_chance/100)
            
            # Display detailed results
            st.success("🎯 Advanced Damage Calculation Results")
            
            # Create metrics in multiple rows
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Base Attack", f"{base_atk:,.0f}")
                st.metric("Step 1 (Modifiers)", f"{step1:,.0f}")
                
            with col2:
                st.metric("Refine Attack", f"{refine_atk:,.0f}")
                st.metric("Step 2 (Race/Pen/Def)", f"{step2:,.0f}")
                
            with col3:
                st.metric("Defense Reduction", f"{def_reduction:.2%}")
                st.metric("Final Non-Crit", f"{step3:,.0f}")
                
            with col4:
                st.metric("Critical Damage", f"{crit_damage:,.0f}")
                st.metric("**Average Damage**", f"{average_damage:,.0f}")

with tab3:
    st.subheader("Damage Comparison Tool")
    st.markdown("*Compare different builds or equipment setups*")
    
    col1, col2 = st.columns(2)
    
    # Build A
    with col1:
        st.markdown("#### 🔴 Build A")
        a_str = st.number_input("STR", min_value=1, max_value=200, value=100, key="a_str")
        a_weapon = st.number_input("Weapon Attack", min_value=0, value=1000, key="a_weapon")
        a_refine = st.number_input("Refine Level", min_value=0, max_value=15, value=0, key="a_refine")
        a_atk_inc = st.number_input("Attack Inc %", min_value=0.0, max_value=1000.0, value=0.0, key="a_atk_inc")
        a_dmg_inc = st.number_input("Damage Inc %", min_value=0.0, max_value=500.0, value=0.0, key="a_dmg_inc")
        a_pen = st.number_input("Penetration %", min_value=0.0, max_value=100.0, value=0.0, key="a_pen")
        
    # Build B
    with col2:
        st.markdown("#### 🔵 Build B")
        b_str = st.number_input("STR", min_value=1, max_value=200, value=120, key="b_str")
        b_weapon = st.number_input("Weapon Attack", min_value=0, value=800, key="b_weapon")
        b_refine = st.number_input("Refine Level", min_value=0, max_value=15, value=5, key="b_refine")
        b_atk_inc = st.number_input("Attack Inc %", min_value=0.0, max_value=1000.0, value=20.0, key="b_atk_inc")
        b_dmg_inc = st.number_input("Damage Inc %", min_value=0.0, max_value=500.0, value=30.0, key="b_dmg_inc")
        b_pen = st.number_input("Penetration %", min_value=0.0, max_value=100.0, value=10.0, key="b_pen")
    
    # Common modifiers for comparison
    st.markdown("#### Common Target & Modifiers")
    col1, col2, col3 = st.columns(3)
    with col1:
        comp_target_def = st.number_input("Target DEF", min_value=0, value=1000, key="comp_def")
    with col2:
        comp_element = st.selectbox("Element Mod", [100, 125, 150, 200], index=0, format_func=lambda x: f"{x}%", key="comp_element")
    with col3:
        comp_race = st.number_input("Race Mod %", min_value=0.0, max_value=200.0, value=100.0, key="comp_race")
    
    if st.button("⚖️ Compare Builds"):
        # Common modifiers
        element_mod_val = comp_element / 100
        race_mod_val = comp_race / 100
        def_reduction = max(0.1, 1 - (comp_target_def / (comp_target_def + 4000)))
        
        # Build A calculation
        a_base_atk = a_weapon + (a_str * 3)
        a_refine_atk = a_refine * 12
        a_atk_inc_mod = 1 + (a_atk_inc / 100)
        a_dmg_inc_mod = 1 + (a_dmg_inc / 100)
        a_pen_reduction = 1 - (a_pen / 100)
        
        a_damage = ((a_base_atk * a_atk_inc_mod * element_mod_val * race_mod_val * def_reduction * a_pen_reduction) + a_refine_atk) * a_dmg_inc_mod
        
        # Build B calculation
        b_base_atk = b_weapon + (b_str * 3)
        b_refine_atk = b_refine * 12
        b_atk_inc_mod = 1 + (b_atk_inc / 100)
        b_dmg_inc_mod = 1 + (b_dmg_inc / 100)
        b_pen_reduction = 1 - (b_pen / 100)
        
        b_damage = ((b_base_atk * b_atk_inc_mod * element_mod_val * race_mod_val * def_reduction * b_pen_reduction) + b_refine_atk) * b_dmg_inc_mod
        
        # Display comparison
        st.success("⚖️ Build Comparison Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🔴 Build A Results")
            st.metric("Base Attack", f"{a_base_atk:,.0f}")
            st.metric("Final Damage", f"{a_damage:,.0f}")
            
        with col2:
            st.markdown("#### 🔵 Build B Results")
            st.metric("Base Attack", f"{b_base_atk:,.0f}")
            st.metric("Final Damage", f"{b_damage:,.0f}")
            
        with col3:
            st.markdown("#### 📊 Comparison")
            damage_diff = b_damage - a_damage
            damage_percent = ((b_damage / a_damage) - 1) * 100 if a_damage > 0 else 0
            
            better_build = "Build B" if damage_diff > 0 else "Build A"
            st.metric("Damage Difference", f"{abs(damage_diff):,.0f}")
            st.metric("Percentage Difference", f"{abs(damage_percent):.1f}%")
            st.success(f"🏆 {better_build} is better!")
            
        # Visualization
        import matplotlib.pyplot as plt
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Damage comparison bar chart
        builds = ['Build A', 'Build B']
        damages = [a_damage, b_damage]
        colors = ['red', 'blue']
        
        ax1.bar(builds, damages, color=colors, alpha=0.7)
        ax1.set_title('Damage Comparison')
        ax1.set_ylabel('Damage')
        ax1.set_ylim(0, max(damages) * 1.1)
        
        # Add value labels on bars
        for i, v in enumerate(damages):
            ax1.text(i, v + max(damages) * 0.01, f'{v:,.0f}', ha='center', va='bottom')
        
        # Component breakdown
        a_components = [a_base_atk, a_refine_atk, (a_damage - a_base_atk - a_refine_atk)]
        b_components = [b_base_atk, b_refine_atk, (b_damage - b_base_atk - b_refine_atk)]
        
        x = range(len(['Base ATK', 'Refine ATK', 'Modifiers']))
        width = 0.35
        
        ax2.bar([i - width/2 for i in x], a_components, width, label='Build A', color='red', alpha=0.7)
        ax2.bar([i + width/2 for i in x], b_components, width, label='Build B', color='blue', alpha=0.7)
        
        ax2.set_title('Component Breakdown')
        ax2.set_ylabel('Damage')
        ax2.set_xticks(x)
        ax2.set_xticklabels(['Base ATK', 'Refine ATK', 'Modifiers'])
        ax2.legend()
        
        plt.tight_layout()
        st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🎮 <strong>Ragnarok M: Eternal Love Damage Calculator</strong></p>
    <p>Based on community-researched damage formulas | Priority: DmgInc > Pen > Crit% > Skill% = Runes% > Race > Size = Element</p>
    <p><em>Note: Results are estimates based on available formulas. Actual in-game values may vary due to hidden mechanics.</em></p>
</div>
""", unsafe_allow_html=True)