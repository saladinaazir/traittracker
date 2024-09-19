import streamlit as st
from itertools import combinations
import os
from PIL import Image
from functools import lru_cache
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple
import json

# ----------------------------
# Data Definitions
# ----------------------------
st.set_page_config(page_title="🛡️ Trait Tracker Solver", layout="wide")
st.title("🛡️ Trait Tracker Solver")
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

# ----------------------------
# Load Pre-solved Combinations
# ----------------------------

@st.cache_data
def load_presolved_combinations(filepath: str) -> List[Dict]:
    if not os.path.exists(filepath):
        st.error(f"Pre-solved combinations file '{filepath}' not found.")
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

pre_solved_combinations = load_presolved_combinations('pre_solved_combinations_extended.json')

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
        if count + emblem_bonus >= required:
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
    filtered_champions = [champ for champ in all_champions if 1 <= champ["cost"] <= 3]

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
   # st.sidebar.subheader("Parameters")
   # min_cost = st.sidebar.number_input("Min Cost:", min_value=1, max_value=5, value=1, step=1)
   # max_cost = st.sidebar.number_input("Max Cost:", min_value=1, max_value=5, value=3, step=1)
    max_num_champions = 7 #st.sidebar.number_input("Max Champions:", min_value=1, max_value=10, value=7, step=1)
    min_traits = 7 #st.sidebar.number_input("Min Traits:", min_value=1, max_value=20, value=7, step=1)

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
            total_possible = len(pre_solved_combinations)
            found_count = 0
            displayed_count = 0
            max_display = 200  # Limit to display first 200 combinations for performance

            # Precompute emblem indices
            emblem_indices = set([trait_to_index[emblem] for emblem in selected_emblems if emblem in trait_to_index])

            # Determine if pre-solved combinations can be used
            no_emblems_selected = len(selected_emblems) == 0

            if no_emblems_selected:
                # Use pre-solved combinations
                for idx, combo in enumerate(pre_solved_combinations):
                    combo_champs = set(combo["Champions"])

                    # 1. Ensure all owned champions are in the combination
                    if not owned_champions.issubset(combo_champs):
                        continue

                    # 2. Ensure no 4 or 5-cost champions are in the combination unless they are owned
                    invalid = False
                    for champ in combo_champs:
                        champ_cost = champion_dict[champ]['cost']
                        if champ_cost >= 4 and champ not in owned_champions:
                            invalid = True
                            break
                    if invalid:
                        continue

                    # 3. Update trait counts
                    trait_counts = [0] * len(all_traits)
                    for champ in combo_champs:
                        for trait in champion_dict[champ]['traits']:
                            if trait in trait_to_index:
                                trait_idx = trait_to_index[trait]
                                trait_counts[trait_idx] += 1

                    # 4. Adjust trait counts based on emblems
                    active_traits = compute_active_traits(tuple(trait_counts), frozenset())

                    # 5. Check if active traits meet the criteria
                    if len(active_traits) >= min_traits:
                        total_cost = sum(champion_dict[name]['cost'] for name in combo_champs)
                        combo_result = {
                            "Champions": combo["Champions"],
                            "Traits": active_traits,
                            "Total Cost": total_cost
                        }
                        matching_combinations.append(combo_result)
                        found_count += 1
                        # Update UI incrementally
                        if displayed_count < max_display:
                            display_combination(combo_result, images, displayed_count + 1)
                            displayed_count += 1
                    # Update progress bar
                    if idx % max(1, total_possible // 100) == 0:  # Update progress based on total
                        progress = idx / total_possible
                        progress_bar.progress(progress)
                status_text.text(f"Found {found_count} combination(s). Displaying first {displayed_count}.")
            else:
                # Use the new combination finding algorithm
                generator = find_compositions(
                    min_cost=1,
                    max_cost=3,
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
                    # Update progress bar
                    if found_count % 10 == 0:
                        progress_bar.progress(min(found_count / 1000, 1.0))
                    if found_count >= 1000:
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
    # st.markdown(f"**Traits:** {', '.join(composition['Traits'])}")
    # st.markdown(f"**Total Cost:** {composition['Total Cost']}")
    # st.markdown("---")

if __name__ == "__main__":
    main()
