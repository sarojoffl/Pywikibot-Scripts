import pywikibot
import re

def add_category_to_articles(file_path, category_name):
    # Set up connection to Nepali Wikipedia
    site = pywikibot.Site('ne', 'wikipedia')
    
    # Descriptive names for category link styles
    nepali_category_link = f"[[श्रेणी:{category_name}]]"
    english_category_link = f"[[Category:{category_name}]]"

    # Regular expression to find existing category links
    category_regex = re.compile(r'\[\[(श्रेणी|Category):[^\]]+\]\]')

    # Read article titles from a file
    with open(file_path, 'r') as file:
        articles = [line.strip() for line in file]

    for article_title in articles:
        try:
            page = pywikibot.Page(site, article_title)
            existing_categories = category_regex.findall(page.text)
            newline_prefix = "\n\n" if not existing_categories else "\n"

            if nepali_category_link not in page.text and english_category_link not in page.text:
                page.text += f"{newline_prefix}{nepali_category_link}"
                page.save(f"Added to category '{category_name}'")
                print(f"Category '{category_name}' added to '{article_title}'")
            else:
                print(f"Category '{category_name}' already present in '{article_title}'")
        except pywikibot.NoPage:
            print(f"Error: Page '{article_title}' does not exist.")
        except pywikibot.IsLockedPage:
            print(f"Error: Page '{article_title}' is locked for editing.")
        except pywikibot.EditConflict:
            print(f"Error: Edit conflict on page '{article_title}'.")
        except pywikibot.ServerError as e:
            print(f"Server error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    file_path = 'article_list.txt'
    category_name = input("Please enter the category name: ")
    add_category_to_articles(file_path, category_name)

