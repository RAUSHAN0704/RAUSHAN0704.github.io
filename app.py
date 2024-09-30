from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Dictionary to map inputType to corresponding Excel files
file_map = {
    'bazaar': 'bazaar_data.csv',
    'office': 'office_data.csv',
    'gramin': 'gramin_data.csv',
    'navyuvak': 'navyuvak_data.csv',
    'patna': 'patna_data.csv'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']
    input_type = request.form['inputType']

    # Get the corresponding file based on the inputType
    excel_file = file_map.get(input_type)
    
    if excel_file:
        # Load the relevant Excel file
        try:
            df = pd.read_csv(excel_file)
        except FileNotFoundError:
            return jsonify({'message': f'File for {input_type} not found'}), 404

        # Check if either 'name' or 'Name' exists in the columns
        name_column = df.filter(like='name', axis=1).columns[0]  # This will capture both 'name' and 'Name'

        # Search the Excel data for the name
        result = df[df[name_column].str.contains(name, case=False, na=False)]

        if result.empty:
            return jsonify({'message': f'No results found for {name} in {input_type}'}), 404
        else:
            # Convert the DataFrame to a dictionary and return as JSON
            result_dict = result.to_dict(orient='records')
            return jsonify(result_dict)
    else:
        return jsonify({'message': 'Invalid input type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
