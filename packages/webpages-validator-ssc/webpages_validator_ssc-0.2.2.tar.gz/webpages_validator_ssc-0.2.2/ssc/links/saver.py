import csv


def save_to_csv(results, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['link', 'code'])
        writer.writerows(results)
