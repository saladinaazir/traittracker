import streamlit as st
from itertools import combinations
import os
from PIL import Image
from functools import lru_cache
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple

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
# Precomputations for Optimization
# ----------------------------

# Assign a unique index to each trait for easy tracking
trait_to_index = {trait['name']: i for i, trait in enumerate(all_traits)}
index_to_trait = {i: trait_name for trait_name, i in trait_to_index.items()}

# Precompute trait requirements
trait_requirements = {}
for trait in all_traits:
    if len(trait['levels']) > 1:
        trait_requirements[trait['name']] = trait['levels'][0]
    else:
        trait_requirements[trait['name']] = None  # Traits with only level 1 cannot be activated

# Precompute champions with trait indices and build a name to champion mapping
champion_dict = {}
for champ in all_champions:
    champ['trait_indices'] = [trait_to_index[trait] for trait in champ['traits'] if trait in trait_to_index]
    champion_dict[champ['name']] = champ

# ----------------------------
# Helper Functions
# ----------------------------

def sort_compositions_by_cost(compositions: List[Dict]) -> List[Dict]:
    """Sort compositions based on total cost."""
    return sorted(compositions, key=lambda combo: combo["Total Cost"])

def load_image(champion_name: str, image_dir='set12icon', placeholder='placeholder.png') -> Image.Image:
    """Load and resize champion image."""
    image_path = os.path.join(image_dir, f"{champion_name}.png")
    if not os.path.exists(image_path):
        image_path = os.path.join(image_dir, placeholder)
    try:
        img = Image.open(image_path)
        img = img.resize((50, 50))
        return img
    except:
        # Return a blank image if failed to load
        return Image.new('RGBA', (50, 50), (255, 0, 0, 255))

@st.cache_resource
def get_images(image_dir='set12icon', placeholder='placeholder.png') -> Dict[str, Image.Image]:
    """Cache champion images to avoid reloading."""
    images = {}
    for champ in all_champions:
        images[champ['name']] = load_image(champ['name'], image_dir, placeholder)
    # Add placeholder image
    images['placeholder.png'] = load_image('placeholder', image_dir, placeholder)
    return images

@lru_cache(maxsize=None)
def compute_active_traits(trait_counts: Tuple[int], emblem_indices: frozenset) -> Tuple[str]:
    """Determine active traits based on trait counts and emblems."""
    active_traits = []
    for trait_name, required in trait_requirements.items():
        if required is None:
            continue  # Traits with only level 1 cannot be activated
        trait_idx = trait_to_index[trait_name]
        count = trait_counts[trait_idx]
        emblem_bonus = 1 if trait_idx in emblem_indices else 0
        required_min = max(required - emblem_bonus, 1)  # Ensure at least 1
        if count >= required_min:
            active_traits.append(trait_name)
    return tuple(active_traits)

def find_compositions(
    min_cost: int,
    max_cost: int,
    max_num_champions: int,
    min_traits: int,
    owned_champions: Set[str],
    selected_emblems: Set[str]
) -> List[Dict]:
    """
    Generator function to find valid champion combinations.

    Yields:
        Dict: A valid combination with champions, traits, and total cost.
    """
    # Filter champions based on cost
    filtered_champions = [champ for champ in all_champions if min_cost <= champ["cost"] <= max_cost]
    
    # Ensure owned champions are within the filtered list
    required_champions = [champion_dict[name] for name in owned_champions if name in champion_dict]
    remaining_champions = [champ for champ in filtered_champions if champ["name"] not in owned_champions]
    
    # Compute emblem indices
    emblem_indices = set([trait_to_index[emblem] for emblem in selected_emblems if emblem in trait_to_index])
    
    # Initialize trait counts and total cost with required champions
    initial_trait_counts = [0] * len(all_traits)
    initial_cost = 0
    for champ in required_champions:
        initial_cost += champ['cost']
        for idx in champ['trait_indices']:
            initial_trait_counts[idx] += 1
    
    # Define backtracking function
    def backtrack(start: int, current_combo: List[Dict], trait_counts: List[int], current_cost: int):
        # Compute active traits
        active_traits = compute_active_traits(tuple(trait_counts), frozenset(emblem_indices))
        active_count = len(active_traits)
        
        # If current combination meets trait requirement, yield it
        if active_count >= min_traits:
            yield {
                "Champions": [champ['name'] for champ in current_combo],
                "Traits": active_traits,
                "Total Cost": current_cost
            }
        
        # If reached maximum number of champions, stop
        if len(current_combo) >= max_num_champions:
            return
        
        for i in range(start, len(remaining_champions)):
            champ = remaining_champions[i]
            new_cost = current_cost + champ['cost']
            new_combo_size = len(current_combo) + 1
            # Check if adding this champion exceeds the max_num_champions or max_cost
            if new_combo_size > max_num_champions or new_cost > max_cost * max_num_champions:
                continue
            # Update trait counts
            new_trait_counts = trait_counts.copy()
            for idx in champ['trait_indices']:
                new_trait_counts[idx] += 1
            # Yield further combinations
            yield from backtrack(i + 1, current_combo + [champ], new_trait_counts, new_cost)
    
    # Start backtracking with required champions
    yield from backtrack(0, required_champions, initial_trait_counts, initial_cost)

# ----------------------------
# Streamlit App
# ----------------------------

def main():
    st.set_page_config(page_title="🛡️ Champion Combination Finder", layout="wide")
    st.title("🛡️ Champion Combination Finder")
    
    # Load images once
    images = get_images()
    
    # Sidebar for Inputs
    st.sidebar.header("🔧 Configure Your Search")
    
    # Trait Emblems
    st.sidebar.subheader("Trait Emblems")
    selectable_emblems = [trait['name'] for trait in all_traits if len(trait['levels']) > 1]
    selected_emblems = set(st.sidebar.multiselect(
        "Select Trait Emblems:",
        options=selectable_emblems,
        default=[]
    ))
    
    # Parameters
    st.sidebar.subheader("Parameters")
    min_cost = st.sidebar.number_input("Min Cost:", min_value=1, max_value=5, value=1, step=1)
    max_cost = st.sidebar.number_input("Max Cost:", min_value=1, max_value=5, value=3, step=1)
    max_num_champions = st.sidebar.number_input("Max Champions:", min_value=1, max_value=10, value=7, step=1)
    min_traits = st.sidebar.number_input("Min Traits:", min_value=1, max_value=20, value=7, step=1)
    
    # Owned Champions
    st.sidebar.subheader("Owned Champions")
    champion_names = sorted([champ['name'] for champ in all_champions])
    owned_champions = set(st.sidebar.multiselect(
        "Select Owned Champions:",
        options=champion_names,
        default=[]
    ))
    
    # Find Combinations Button
    if st.sidebar.button("Find Combinations"):
        with st.spinner("Searching for valid combinations..."):
            # Initialize placeholders for dynamic content
            result_placeholder = st.empty()
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            matching_combinations = []
            total_possible = 1000  # Adjust based on expected number of combinations
            found_count = 0
            displayed_count = 0
            max_display = 200  # Limit to display first 20 combinations for performance
            
            # Function to process pre-solved combinations
            def process_pre_solved():
                for combo in pre_solved_combinations:
                    # Check if owned champions are subset of this combo
                    if owned_champions.issubset(set(combo["Champions"])):
                        # Check cost constraints
                        total_cost = sum(
                            champion_dict[name]['cost'] for name in combo["Champions"] if name in champion_dict
                        )
                        if min_cost <= total_cost <= max_cost * max_num_champions:
                            # Check trait constraints
                            active_traits = combo["Traits"]
                            if len(active_traits) >= min_traits:
                                yield {
                                    "Champions": combo["Champions"],
                                    "Traits": active_traits,
                                    "Total Cost": total_cost
                                }
            
            # Determine if pre-solved combinations can be used
            all_owned_within_cost = all(
                min_cost <= champion_dict[name]['cost'] <= max_cost
                for name in owned_champions
                if name in champion_dict
            )
            no_emblems_selected = len(selected_emblems) == 0
            
            if all_owned_within_cost and no_emblems_selected:
                # Use pre-solved combinations
                for combo in process_pre_solved():
                    matching_combinations.append(combo)
                    found_count += 1
                    # Update UI incrementally
                    if displayed_count < max_display:
                        display_combination(combo, images, displayed_count + 1)
                        displayed_count += 1
                        progress_bar.progress(found_count / total_possible)
                status_text.text(f"Found {found_count} combination(s). Displaying first {displayed_count}.")
            else:
                # Use the new combination finding algorithm
                generator = find_compositions(
                    min_cost=min_cost,
                    max_cost=max_cost,
                    max_num_champions=max_num_champions,
                    min_traits=min_traits,
                    owned_champions=owned_champions,
                    selected_emblems=selected_emblems
                )
                for combo in generator:
                    matching_combinations.append(combo)
                    found_count += 1
                    # Update UI incrementally
                    if displayed_count < max_display:
                        display_combination(combo, images, displayed_count + 1)
                        displayed_count += 1
                        progress_bar.progress(found_count / total_possible)
                    if found_count >= total_possible:
                        break
                status_text.text(f"Found {found_count} combination(s). Displaying first {displayed_count}.")
            
            # Final status
            if found_count == 0:
                result_placeholder.warning("No valid combinations found based on the selected criteria.")
            else:
                if found_count > max_display:
                    result_placeholder.warning(f"Found {found_count} valid combinations. Displaying first {max_display}.")
                elif found_count <= max_display:
                    result_placeholder.success(f"Found {found_count} valid combination(s).")
                # Remove progress bar and status text
                progress_bar.empty()
                status_text.empty()

def display_combination(composition: Dict, images: Dict[str, Image.Image], idx: int):
    """Display a single combination with images side by side."""
   # st.markdown(f"### Combination {idx}")
    
    # Collect the images and captions
    champion_images = [images.get(champ_name, images.get('placeholder.png')) for champ_name in composition['Champions']]
    champion_captions = composition['Champions']
    
    # Display images horizontally with captions
    st.image(champion_images, width=80, caption=champion_captions, use_column_width=False)
    
    # Display traits and total cost
    #st.markdown(f"**Traits:** {', '.join(composition['Traits'])}")
    #st.markdown(f"**Total Cost:** {composition['Total Cost']}")
   # st.markdown("---")

if __name__ == "__main__":
    main()
