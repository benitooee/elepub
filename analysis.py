import csv
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

script_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_dir, 'word.csv')

# Folder to save plots
plots_dir = os.path.join(script_dir, 'plots')
os.makedirs(plots_dir, exist_ok=True)

# Failure rate of LLMs answering the questions
total_failure = 3 * 17  # 3 responses could not answer any question at all (17 questions)
not_specified_count = 0

people_data = {
    'Stephanie Lee': [],
    'Raymond Lau': [],
    'Jason Lam': [],
    'Samuel Ng': [],
    'Li Wei': []
}

try:
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        # Skip the header line
        try:
            header = next(reader)
            print("Header:", header)
        except StopIteration:
            print("File is empty")
            header = []
        
        for column in reader:
            for cell in column:
                if cell.strip().lower() == "not specified":
                    not_specified_count += 1

            if len(column) >= 17:
                name = column[0]
                budget = column[1]
                current_pets = column[2]
                adopt_before = column[3]
                adopt_better = column[4]
                responsibility = column[5]
                breed = column[6]
                reason = column[7]
                alone = column[8]
                financial = column[9]
                activity = column[10]
                consent = column[11]
                outdoors = column[12]
                home = column[13]
                people = column[14]
                children = column[15]
                elderly = column[16]
                baby = column[17]

                print(
                    f"name: {name}, budget: {budget}, current_pets:{current_pets}, "
                    f"adopt_before: {adopt_before}, adopt_better: {adopt_better}, responsibility: {responsibility}, "
                    f"breed: {breed}, reason: {reason}, alone: {alone}, financial: {financial}, activity: {activity}, "
                    f"consent: {consent}, outdoors: {outdoors}, home: {home}, people: {people}, children: {children}, "
                    f"elderly: {elderly}, baby: {baby}"
                )

                if name in people_data:
                    people_data[name].append({
                        'budget': budget,
                        'current_pets': current_pets,
                        'adopt_before': adopt_before,
                        'adopt_better': adopt_better,
                        'responsibility': responsibility,
                        'breed': breed,
                        'reason': reason,
                        'alone': alone,
                        'financial': financial,
                        'activity': activity,
                        'consent': consent,
                        'outdoors': outdoors,
                        'home': home,
                        'people': people,
                        'children': children,
                        'elderly': elderly,
                        'baby': baby
                    })

            else:
                print(f"Warning: Line doesn't have enough columns: {column}")

    All_Failure = total_failure + not_specified_count
    print(f"\nTotal number of values saying 'Not Specified': {not_specified_count}")
    print(f"Total 'Not Specified' occurrences: {not_specified_count}")
    print(f"Questions completely unanswered (3 responses × 17 questions): {total_failure}")
    print(f"Questions completely unanswered (3 responses × 17 questions): {total_failure}")
    print(f"Total unanswered questions: {All_Failure}")

    # Pie chart
    plt.figure()
    plt.pie([All_Failure, 1683 - All_Failure],
            labels=['Failure', 'Completed'], autopct='%1.1f%%')
    plt.title('Total: 1683')
    pie_path = os.path.join(plots_dir, 'pie_chart.png')
    plt.savefig(pie_path, dpi=300, bbox_inches='tight')
    plt.close()

    # Scatter plots
    budget_categories = ['Less than $50', '$50-$100', '$100-$200', 'Over $200']

    def create_budget_scatter(ax, budget_list, title):
        counts = {cat: 0 for cat in budget_categories}
        scatter_data = {cat: [] for cat in budget_categories}

        for budget in budget_list:
            if budget in counts:
                counts[budget] += 1
                scatter_data[budget].append(counts[budget])

        for i, cat in enumerate(budget_categories):
            if scatter_data[cat]:
                x_jitter = np.random.normal(i + 1, 0.04, len(scatter_data[cat]))
                ax.scatter(x_jitter, scatter_data[cat], alpha=0.6, s=100, color='blue')

        all_counts = [c for c in counts.values() if c > 0]
        if all_counts:
            median_val = np.median(all_counts)
            ax.axhline(y=median_val, color='red', linestyle='--', linewidth=2,
                       label=f'Median: {median_val:.1f}')

        if len(all_counts) >= 2:
            q1 = np.percentile(all_counts, 25)
            q3 = np.percentile(all_counts, 75)
            ax.axhspan(q1, q3, alpha=0.2, color='green', label=f'IQR: {q1:.1f}-{q3:.1f}')

        ax.set_xticks(range(1, len(budget_categories) + 1))
        ax.set_xticklabels(budget_categories, rotation=45, ha='right')
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Budget Category')
        ax.set_title(title, fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

    # Overall budget scatter
    fig_overall, ax_overall = plt.subplots(figsize=(12, 6))
    all_budgets = []
    for person_data_list in people_data.values():
        for data in person_data_list:
            if data['budget'] not in ['Not specified', '']:
                all_budgets.append(data['budget'])

    create_budget_scatter(ax_overall, all_budgets, 'Budget Distribution - All People')
    plt.tight_layout()
    overall_path = os.path.join(plots_dir, 'budget_overall.png')
    fig_overall.savefig(overall_path, dpi=300, bbox_inches='tight')
    plt.close(fig_overall)

    # Budget distribution by person
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Budget Distribution by Person', fontsize=16)
    axes = axes.flatten()

    for idx, (person_name, data_list) in enumerate(people_data.items()):
        if idx < len(axes):
            person_budgets = [data['budget'] for data in data_list
                              if data['budget'] not in ['Not specified', '']]
            create_budget_scatter(axes[idx], person_budgets, person_name)

    if len(people_data) < len(axes):
        axes[len(people_data)].axis('off')

    plt.tight_layout()
    by_person_path = os.path.join(plots_dir, 'budget_by_person.png')
    fig.savefig(by_person_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Heatmap
    activity_categories = ['Low - calm and cuddly',
                           'Medium - enjoys daily play',
                           'High - very energetic']
    alone_categories = ['0-4 hours', '5-8 hours', '9+ hours']

    all_activity = []
    all_alone = []

    with open(filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        for column in reader:
            if len(column) >= 11:
                activity = column[10]  # Activity level
                alone = column[8]      # Alone time

                if activity in activity_categories and alone in alone_categories:
                    all_activity.append(activity)
                    all_alone.append(alone)

    activity_indices = {cat: i for i, cat in enumerate(activity_categories)}
    alone_indices = {cat: i for i, cat in enumerate(alone_categories)}

    heatmap_matrix = np.zeros((3, 3))
    for act, alone in zip(all_activity, all_alone):
        heatmap_matrix[activity_indices[act], alone_indices[alone]] += 1

    fig_hm, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        heatmap_matrix, annot=True, fmt='g', cmap='YlOrRd', ax=ax,
        xticklabels=alone_categories,
        yticklabels=activity_categories,
        cbar_kws={'label': 'Frequency'}
    )
    ax.set_xlabel('Hours Alone per Day')
    ax.set_ylabel('Activity Level')
    ax.set_title('Heatmap: Activity Level vs Hours Alone')
    plt.tight_layout()
    heatmap_path = os.path.join(plots_dir, 'heatmap_activity_vs_alone.png')
    fig_hm.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    plt.close(fig_hm)

except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
