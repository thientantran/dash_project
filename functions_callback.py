import functions
def update_output_1_input(content, name, date):
    if content is not None:
        children = functions.parse_contents(content, name, date)
        return children

def update_output_multi_input(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            functions.parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children