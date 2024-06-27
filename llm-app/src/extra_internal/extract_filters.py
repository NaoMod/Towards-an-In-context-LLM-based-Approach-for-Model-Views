import re
import json

def extract_select_part(code):
    # Initialize an empty dictionary to store the extracted fields
    select_dict = {"filters": {}}
    
    # Regular expression patterns to match SELECT statements and column names
    select_pattern = re.compile(r'select\s+(.*?)\s+from', re.IGNORECASE | re.DOTALL)
    column_pattern = re.compile(r'([a-zA-Z0-9_]+)\.([a-zA-Z0-9_*]+)\.([a-zA-Z0-9_*]+)')

    # Find the SELECT part using regex
    select_match = select_pattern.search(code)
    if select_match:
        select_part = select_match.group(1).strip()
        columns = select_part.split(',')
        
        # Iterate through each column and extract table and column names
        for column in columns:
            column_match = column_pattern.search(column.strip())
            if column_match:
                meta_name = column_match.group(1)
                table_name = column_match.group(2)
                column_name = column_match.group(3)
                
                # Add table, column, and meta to the dictionary
                if meta_name not in select_dict["filters"]:
                    select_dict["filters"][meta_name] = {}
                if table_name not in select_dict["filters"][meta_name]:
                    select_dict["filters"][meta_name][table_name] = []
                select_dict["filters"][meta_name][table_name].append(column_name)

    # Convert the dictionary to JSON and return
    return json.dumps(select_dict, indent=4)

if __name__ == "__main__":
    # Example usage:
    code = """
    select publication.Publication.*,
        book.Book.*,
        book.Book.title,
        book.Chapter.title,
        publication.Publication join book.Chapter as firstChapter,
        publication.Publication join book.Chapter as bookChapters,

    from 'http://publication' as publication,
        'http://book' as book,

    where s.title = t.eContainer().title
        and t = t.eContainer().chapters.first()
        for firstChapter,
        s.title = t.eContainer().title
        for bookChapters
        
    """

    # Call the function and print the result
    print(extract_select_part(code))

