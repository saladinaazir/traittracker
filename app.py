import streamlit as st
from itertools import combinations
import math
import os
from PIL import Image
from collections import defaultdict
import sys
import base64

# ----------------------------
# Data Definitions
# ----------------------------

all_champions = [
    {"name": "Zoe", "cost": 1, "traits": ["Portal", "Witchcraft", "Scholar"]},
    {"name": "Ziggs", "cost": 1, "traits": ["Honeymancy", "Incantor"]},
    {"name": "Warwick", "cost": 1, "traits": ["Frost", "Vanguard"]},
    {"name": "Twitch", "cost": 1, "traits": ["Frost", "Hunter"]},
    {"name": "Soraka", "cost": 1, "traits": ["Sugarcraft", "Mage"]},
    {"name": "Seraphine", "cost": 1, "traits": ["Faerie", "Mage"]},
    {"name": "Poppy", "cost": 1, "traits": ["Witchcraft", "Bastion"]},
    {"name": "Nomsy", "cost": 1, "traits": ["Dragon", "Hunter"]},
    {"name": "Lillia", "cost": 1, "traits": ["Faerie", "Bastion"]},
    {"name": "Jayce", "cost": 1, "traits": ["Portal", "Shapeshifter"]},
    {"name": "Jax", "cost": 1, "traits": ["Chrono", "Multistriker"]},
    {"name": "Elise", "cost": 1, "traits": ["Eldritch", "Shapeshifter"]},
    {"name": "Blitzcrank", "cost": 1, "traits": ["Honeymancy", "Vanguard"]},
    {"name": "Ashe", "cost": 1, "traits": ["Eldritch", "Multistriker"]},
    {"name": "Zilean", "cost": 2, "traits": ["Frost", "Chrono", "Preserver"]},
    {"name": "Tristana", "cost": 2, "traits": ["Faerie", "Blaster"]},
    {"name": "Syndra", "cost": 2, "traits": ["Eldritch", "Incantor"]},
    {"name": "Shyvana", "cost": 2, "traits": ["Dragon", "Shapeshifter"]},
    {"name": "Rumble", "cost": 2, "traits": ["Sugarcraft", "Vanguard", "Blaster"]},
    {"name": "Nunu", "cost": 2, "traits": ["Honeymancy", "Bastion"]},
    {"name": "Nilah", "cost": 2, "traits": ["Eldritch", "Warrior"]},
    {"name": "Kog'Maw", "cost": 2, "traits": ["Honeymancy", "Hunter"]},
    {"name": "Kassadin", "cost": 2, "traits": ["Portal", "Multistriker"]},
    {"name": "Galio", "cost": 2, "traits": ["Portal", "Vanguard", "Mage"]},
    {"name": "Cassiopeia", "cost": 2, "traits": ["Witchcraft", "Incantor"]},
    {"name": "Akali", "cost": 2, "traits": ["Pyro", "Warrior", "Multistriker"]},
    {"name": "Ahri", "cost": 2, "traits": ["Arcana", "Scholar"]},
    {"name": "Wukong", "cost": 3, "traits": ["Druid"]},
    {"name": "Vex", "cost": 3, "traits": ["Chrono", "Mage"]},
    {"name": "Veigar", "cost": 3, "traits": ["Honeymancy", "Mage"]},
    {"name": "Swain", "cost": 3, "traits": ["Frost", "Shapeshifter"]},
    {"name": "Shen", "cost": 3, "traits": ["Pyro", "Bastion"]},
    {"name": "Neeko", "cost": 3, "traits": ["Witchcraft", "Shapeshifter"]},
    {"name": "Mordekaiser", "cost": 3, "traits": ["Eldritch", "Vanguard"]},
    {"name": "Katarina", "cost": 3, "traits": ["Faerie", "Warrior"]},
    {"name": "Jinx", "cost": 3, "traits": ["Sugarcraft", "Hunter"]},
    {"name": "Hwei", "cost": 3, "traits": ["Frost", "Blaster"]},
    {"name": "Hecarim", "cost": 3, "traits": ["Arcana", "Bastion", "Multistriker"]},
    {"name": "Ezreal", "cost": 3, "traits": ["Portal", "Blaster"]},
    {"name": "Bard", "cost": 3, "traits": ["Sugarcraft", "Preserver", "Scholar"]},
    {"name": "Varus", "cost": 4, "traits": ["Pyro", "Blaster"]},
    {"name": "Taric", "cost": 4, "traits": ["Portal", "Bastion"]},
    {"name": "TahmKench", "cost": 4, "traits": ["Arcana", "Vanguard"]},
    {"name": "Ryze", "cost": 4, "traits": ["Portal", "Incantor"]},
    {"name": "Rakan", "cost": 4, "traits": ["Faerie", "Preserver"]},
    {"name": "Olaf", "cost": 4, "traits": ["Frost", "Hunter"]},
    {"name": "Nasus", "cost": 4, "traits": ["Pyro", "Shapeshifter"]},
    {"name": "Nami", "cost": 4, "traits": ["Eldritch", "Mage"]},
    {"name": "Karma", "cost": 4, "traits": ["Chrono", "Incantor"]},
    {"name": "Kalista", "cost": 4, "traits": ["Faerie", "Multistriker"]},
    {"name": "Gwen", "cost": 4, "traits": ["Sugarcraft", "Warrior"]},
    {"name": "Fiora", "cost": 4, "traits": ["Witchcraft", "Warrior"]},
    {"name": "Xerath", "cost": 5, "traits": ["Arcana", "Ascendant"]},
    {"name": "Smolder", "cost": 5, "traits": ["Dragon", "Blaster"]},
    {"name": "NorraYuumi", "cost": 5, "traits": ["Portal", "Mage"]},
    {"name": "Morgana", "cost": 5, "traits": ["Witchcraft", "Preserver"]},
    {"name": "Milio", "cost": 5, "traits": ["Faerie", "Scholar"]},
    {"name": "Diana", "cost": 5, "traits": ["Frost", "Bastion"]},
    {"name": "Camille", "cost": 5, "traits": ["Chrono", "Multistriker"]},
    {"name": "Briar", "cost": 5, "traits": ["Eldritch", "Ravenous", "Shapeshifter"]}
]

all_traits = [
    {"name": "Arcana", "levels": [2, 3, 4, 5]},
    {"name": "Chrono", "levels": [2, 4, 6]},
    {"name": "Dragon", "levels": [2, 3]},
    {"name": "Druid", "levels": [1]},
    {"name": "Eldritch", "levels": [3, 5, 7, 10]},
    {"name": "Faerie", "levels": [3, 5, 7, 9]},
    {"name": "Frost", "levels": [3, 5, 7, 9]},
    {"name": "Honeymancy", "levels": [3, 5, 7]},
    {"name": "Portal", "levels": [3, 6, 8, 10]},
    {"name": "Pyro", "levels": [2, 3, 4, 5]},
    {"name": "Ravenous", "levels": [1]},
    {"name": "Sugarcraft", "levels": [2, 4, 6]},
    {"name": "Witchcraft", "levels": [2, 4, 6, 8]},
    {"name": "Ascendant", "levels": [1]},
    {"name": "Bastion", "levels": [2, 4, 6, 8]},
    {"name": "Bat Queen", "levels": [1]},
    {"name": "Best Friends", "levels": [1]},
    {"name": "Blaster", "levels": [2, 4, 6]},
    {"name": "Hunter", "levels": [2, 4, 6]},
    {"name": "Incantor", "levels": [2, 4]},
    {"name": "Mage", "levels": [3, 5, 7, 9]},
    {"name": "Multistriker", "levels": [3, 5, 7]},
    {"name": "Preserver", "levels": [2, 3, 4, 5]},
    {"name": "Scholar", "levels": [2, 4, 6]},
    {"name": "Shapeshifter", "levels": [2, 4, 6, 8]},
    {"name": "Vanguard", "levels": [2, 4, 6]},
    {"name": "Warrior", "levels": [2, 4, 6]}
]

pre_solved_combinations = [
    {"Champions": ["Bard", "Ezreal", "Galio", "Rumble", "Lillia", "Poppy", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Vanguard", "Bastion", "Witchcraft"]},
    {"Champions": ["Bard", "Hwei", "Rumble", "Zilean", "Jax", "Warwick", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Frost", "Blaster", "Vanguard", "Chrono"]},
    {"Champions": ["Bard", "Hwei", "Rumble", "Zilean", "Poppy", "Warwick", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Frost", "Blaster", "Vanguard", "Witchcraft"]},
    {"Champions": ["Bard", "Ezreal", "Neeko", "Rumble", "Blitzcrank", "Jayce", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Witchcraft", "Shapeshifter", "Vanguard"]},
    {"Champions": ["Bard", "Ezreal", "Neeko", "Rumble", "Jayce", "Warwick", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Witchcraft", "Shapeshifter", "Vanguard"]},
    {"Champions": ["Bard", "Ezreal", "Cassiopeia", "Galio", "Rumble", "Ziggs", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Witchcraft", "Incantor", "Vanguard"]},
    {"Champions": ["Bard", "Ezreal", "Galio", "Nunu", "Rumble", "Poppy", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Vanguard", "Bastion", "Witchcraft"]},
    {"Champions": ["Bard", "Ezreal", "Galio", "Rumble", "Zilean", "Jax", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Portal", "Blaster", "Vanguard", "Chrono"]},
    {"Champions": ["Bard", "Ezreal", "Galio", "Rumble", "Zilean", "Poppy", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Portal", "Blaster", "Vanguard", "Witchcraft"]},
    {"Champions": ["Bard", "Hwei", "Ahri", "Rumble", "Zilean", "Jax", "Warwick"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Frost", "Blaster", "Vanguard", "Chrono"]},
    {"Champions": ["Bard", "Hwei", "Cassiopeia", "Rumble", "Zilean", "Warwick", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Frost", "Blaster", "Witchcraft", "Vanguard"]},
    {"Champions": ["Bard", "Neeko", "Galio", "Rumble", "Tristana", "Jayce", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Witchcraft", "Shapeshifter", "Portal", "Vanguard", "Blaster"]},
    {"Champions": ["Bard", "Neeko", "Galio", "Rumble", "Zilean", "Jayce", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Witchcraft", "Shapeshifter", "Portal", "Vanguard"]},
    {"Champions": ["Ezreal", "Hecarim", "Ahri", "Galio", "Rumble", "Poppy", "Zoe"], "Traits": ["Portal", "Blaster", "Arcana", "Bastion", "Scholar", "Vanguard", "Witchcraft"]},
    {"Champions": ["Ezreal", "Jinx", "Galio", "Rumble", "Shyvana", "Jayce", "Nomsy"], "Traits": ["Portal", "Blaster", "Sugarcraft", "Hunter", "Vanguard", "Dragon", "Shapeshifter"]},
    {"Champions": ["Bard", "Ezreal", "Hecarim", "Galio", "Rumble", "Poppy", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Bastion", "Vanguard", "Witchcraft"]},
    {"Champions": ["Bard", "Ezreal", "Neeko", "Galio", "Rumble", "Elise", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Witchcraft", "Shapeshifter", "Vanguard"]},
    {"Champions": ["Bard", "Ezreal", "Neeko", "Galio", "Rumble", "Jayce", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Witchcraft", "Shapeshifter", "Vanguard"]},
    {"Champions": ["Bard", "Ezreal", "Neeko", "Rumble", "Zilean", "Jayce", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Portal", "Blaster", "Witchcraft", "Shapeshifter"]},
    {"Champions": ["Bard", "Ezreal", "Shen", "Galio", "Rumble", "Poppy", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Bastion", "Vanguard", "Witchcraft"]},
    {"Champions": ["Bard", "Ezreal", "Cassiopeia", "Galio", "Rumble", "Syndra", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Witchcraft", "Incantor", "Vanguard"]},
    {"Champions": ["Bard", "Ezreal", "Cassiopeia", "Galio", "Rumble", "Zilean", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Portal", "Blaster", "Witchcraft", "Vanguard"]},
    {"Champions": ["Bard", "Hwei", "Neeko", "Galio", "Rumble", "Jayce", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Blaster", "Witchcraft", "Shapeshifter", "Portal", "Vanguard"]},
    {"Champions": ["Bard", "Hwei", "Neeko", "Rumble", "Zilean", "Warwick", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Frost", "Blaster", "Witchcraft", "Vanguard"]},
    {"Champions": ["Bard", "Hwei", "Vex", "Rumble", "Zilean", "Warwick", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Frost", "Blaster", "Chrono", "Vanguard"]},
    {"Champions": ["Bard", "Jinx", "Neeko", "Shyvana", "Zilean", "Nomsy", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Hunter", "Witchcraft", "Shapeshifter", "Dragon"]},
    {"Champions": ["Bard", "Neeko", "Swain", "Rumble", "Zilean", "Warwick", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Witchcraft", "Shapeshifter", "Frost", "Vanguard"]},
    {"Champions": ["Hwei", "Jinx", "Swain", "Rumble", "Shyvana", "Nomsy", "Warwick"], "Traits": ["Frost", "Blaster", "Sugarcraft", "Hunter", "Shapeshifter", "Vanguard", "Dragon"]},
    {"Champions": ["Bard", "Ezreal", "Mordekaiser", "Neeko", "Rumble", "Jayce", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Vanguard", "Witchcraft", "Shapeshifter"]},
    {"Champions": ["Bard", "Ezreal", "Neeko", "Galio", "Rumble", "Shyvana", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Witchcraft", "Shapeshifter", "Vanguard"]},
    {"Champions": ["Bard", "Ezreal", "Neeko", "Galio", "Rumble", "Zilean", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Portal", "Blaster", "Witchcraft", "Shapeshifter", "Vanguard"]},
    {"Champions": ["Bard", "Ezreal", "Vex", "Galio", "Rumble", "Zilean", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Portal", "Blaster", "Chrono", "Vanguard"]},
    {"Champions": ["Bard", "Hecarim", "Hwei", "Ahri", "Rumble", "Zilean", "Warwick"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Arcana", "Frost", "Blaster", "Vanguard"]},
    {"Champions": ["Bard", "Hecarim", "Shen", "Ahri", "Akali", "Zilean", "Jax"], "Traits": ["Preserver", "Scholar", "Arcana", "Bastion", "Multistriker", "Pyro", "Chrono"]},
    {"Champions": ["Bard", "Hwei", "Neeko", "Swain", "Rumble", "Warwick", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Frost", "Blaster", "Witchcraft", "Shapeshifter", "Vanguard"]},
    {"Champions": ["Bard", "Hwei", "Vex", "Ahri", "Rumble", "Zilean", "Warwick"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Frost", "Blaster", "Chrono", "Vanguard"]},
    {"Champions": ["Bard", "Jinx", "Neeko", "Swain", "Zilean", "Twitch", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Hunter", "Witchcraft", "Shapeshifter", "Frost"]},
    {"Champions": ["Bard", "Ezreal", "Neeko", "Swain", "Galio", "Rumble", "Zoe"], "Traits": ["Sugarcraft", "Scholar", "Portal", "Blaster", "Witchcraft", "Shapeshifter", "Vanguard"]},
    {"Champions": ["Bard", "Hwei", "Neeko", "Swain", "Rumble", "Zilean", "Zoe"], "Traits": ["Sugarcraft", "Preserver", "Scholar", "Frost", "Blaster", "Witchcraft", "Shapeshifter"]}
]

# ----------------------------
# Helper Functions
# ----------------------------

def is_trait_active(trait_counts, trait_name, emblem_traits=[]):
    trait = next((trait for trait in all_traits if trait['name'] == trait_name), None)
    if not trait:
        return False
    if trait["levels"] == [1]:
        return False
    required_count = trait["levels"][0]
    emblem_bonus = emblem_traits.count(trait_name)
    required_count -= emblem_bonus
    return trait_counts.get(trait_name, 0) >= required_count

def sort_compositions_by_cost(compositions):
    return sorted(compositions, key=lambda combo: sum(
        next((champ['cost'] for champ in all_champions if champ['name'] == name), 0) for name in combo["Champions"]
    ))

def find_compositions(min_cost, max_cost, max_num_champions, min_traits, current_champions_name=[], emblem_traits=[]):
    filtered_champions = [champ for champ in all_champions if min_cost <= champ["cost"] <= max_cost]

    required_champions = [champion for champion in all_champions if champion['name'] in current_champions_name]
    remaining_champions = [champion for champion in filtered_champions if champion["name"] not in current_champions_name]

    max_remaining_champions = max_num_champions - len(required_champions)
    if max_remaining_champions < 0:
        return []

    results = []

    for num in range(1, max_remaining_champions + 1):
        for combo in combinations(remaining_champions, num):
            full_combo = tuple(required_champions) + combo
            trait_counts = defaultdict(int)
            for champ in full_combo:
                for trait in champ["traits"]:
                    trait_counts[trait] += 1

            active_traits = [trait for trait in trait_counts if is_trait_active(trait_counts, trait, emblem_traits)]

            if len(active_traits) >= min_traits:
                composition = {"Champions": [champ['name'] for champ in full_combo], "Traits": active_traits}
                results.append(composition)
    return results

def load_image(champion_name, image_dir='set12icon', placeholder='placeholder.png'):
    image_path = os.path.join(image_dir, f"{champion_name}.png")
    if not os.path.exists(image_path):
        image_path = os.path.join(image_dir, placeholder)
    try:
        img = Image.open(image_path)
        img = img.resize((50, 50))
        return img
    except:
        # Return a blank image if failed to load
        img = Image.new('RGBA', (50, 50), (255, 0, 0, 255))
        return img

def get_image_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# ----------------------------
# Streamlit App
# ----------------------------

def main():
    st.set_page_config(page_title="Champion Combination Finder", layout="wide")
    st.title("🛡️ Champion Combination Finder")

    # Sidebar for Inputs
    st.sidebar.header("🔧 Configure Your Search")

    # Trait Emblems
    st.sidebar.subheader("Trait Emblems")
    selected_emblems = st.sidebar.multiselect(
        "Select Trait Emblems:",
        options=[trait['name'] for trait in all_traits if trait['levels'] != [1]],
        default=[]
    )

    # Parameters
    st.sidebar.subheader("Parameters")
    min_cost = st.sidebar.number_input("Min Cost:", min_value=1, max_value=5, value=1, step=1)
    max_cost = st.sidebar.number_input("Max Cost:", min_value=1, max_value=5, value=3, step=1)
    max_num_champions = st.sidebar.number_input("Max Champions:", min_value=1, max_value=10, value=7, step=1)
    min_traits = st.sidebar.number_input("Min Traits:", min_value=1, max_value=20, value=7, step=1)

    # Owned Champions
    st.sidebar.subheader("Owned Champions")
    champion_names = sorted([champ['name'] for champ in all_champions])
    owned_champions = st.sidebar.multiselect(
        "Select Owned Champions:",
        options=champion_names,
        default=[]
    )

    # Find Combinations Button
    if st.sidebar.button("Find Combinations"):
        with st.spinner("Searching for valid combinations..."):
            # Check if all owned champions are cost <=3 and no emblems selected
            all_owned_cost_le_3 = all(
                next((champ['cost'] for champ in all_champions if champ['name'] == name), 0) <= 3
                for name in owned_champions
            )
            no_emblems_selected = len(selected_emblems) == 0

            matching_combinations = []

            if all_owned_cost_le_3 and no_emblems_selected:
                # Use pre-solved combinations
                for combo in pre_solved_combinations:
                    if set(owned_champions).issubset(set(combo["Champions"])):
                        if len(combo["Champions"]) <= max_num_champions:
                            matching_combinations.append(combo)
            else:
                # Use normal combination finding
                matching_combinations = find_compositions(
                    min_cost=min_cost,
                    max_cost=max_cost,
                    max_num_champions=max_num_champions,
                    min_traits=min_traits,
                    current_champions_name=owned_champions,
                    emblem_traits=selected_emblems
                )

            if not matching_combinations:
                st.warning("No valid combinations found based on the selected criteria.")
            else:
                # Sort by total cost
                sorted_combinations = sort_compositions_by_cost(matching_combinations)
                st.success(f"Found {len(sorted_combinations)} valid combinations.")

                # Display Results
                for idx, composition in enumerate(sorted_combinations, 1):
                    st.markdown(f"### Combination {idx}")
                    cols = st.columns(len(composition['Champions']))
                    for col, champ_name in zip(cols, composition['Champions']):
                        img = load_image(champ_name)
                        with col:
                            st.image(img, width=50)
                            st.caption(champ_name)
                    st.markdown(f"**Traits:** {', '.join(composition['Traits'])}")
                    total_cost = sum(
                        next((champ['cost'] for champ in all_champions if champ['name'] == name), 0)
                        for name in composition['Champions']
                    )
                    st.markdown(f"**Total Cost:** {total_cost}")
                    st.markdown("---")

if __name__ == "__main__":
    main()
