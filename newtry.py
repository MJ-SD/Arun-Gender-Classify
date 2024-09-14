import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output  # Import Input and Output for callbacks
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from dash import dcc
from dash import html
import plotly.express as px
app = dash.Dash(__name__, assets_folder='pro_dash/assets')

# Load your dataset
df = pd.read_csv(r'exploded_authors_no_authors_predicted_genders (2).csv')

# Create Dash app
app = dash.Dash(__name__)

# Define color mapping for genders
color_map = {
    'male': 'blue',
    'female': 'pink',
    'unisex': 'green',
    'unknown': 'gray'
}

# Define the layout of the app
app.layout = html.Div([
    # Title with light background and gradient text for gender diversity
    html.Div([
        html.H1('VISUALIZING HISTORICAL GENDER DIVERSITY IN CS PUBLICATIONS',
                style={
                    'textAlign': 'center', 
                    'backgroundColor': '#f7f7f7',  # Light background
                    'padding': '20px',
                    'color': 'white',
                    'backgroundImage': 'linear-gradient(to right, blue, pink, green, gray)',
                    '-webkit-background-clip': 'text',
                    'color': 'transparent'
                }),
       
    ], id='home'),

    # Navigation buttons aligned horizontally below title
    html.Div([
        html.Button('Home', id='home-button', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'  # No border, curved edges
        }),
        html.Button('Overall Gender Distribution', id='overall-button', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        }),
        html.Button('Gender Distribution Over the Years', id='years-button', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        }),
        html.Button('Popularity vs Gender Diversity', id='popularity-button', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        }),
        html.Button('Top Authors by Gender', id='top-authors-button', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        }),
        html.Button('About', id='about-button', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        })
    ], style={'textAlign': 'center', 'margin': '20px 0'}),

    # Overall Gender Distribution visualization
    html.Div([
        html.H2('Overall Gender Distribution in CS Publications', style={'textAlign': 'center'}),
        dcc.Graph(id='overall-gender-dist', figure={}),
    ], id='overall-gender'),

    # Gender Distribution Over the Years visualization
    html.Div([
        html.H2('Gender Distribution Over the Years', style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='dropdown-venue',
            placeholder="Select a Conference",
            value=None,
            style={'width': '60%', 'margin': '20px auto'}
        ),
        dcc.Graph(id='gender-dist-years'),
    ], id='gender-years'),

    # Popularity vs Gender Diversity visualization
    html.Div([
        html.H2('Conference Popularity vs Gender Diversity', style={'textAlign': 'center'}),
        dcc.Graph(id='popularity-gender-dist', figure={}),
    ], id='popularity-gender'),

    # Top Authors by Gender visualization
    # Add a dropdown to select the number of authors to display
    html.Div([
    html.H3('Top Authors by Gender', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='num-authors-dropdown',
        options=[
            {'label': 'Top 10 Authors', 'value': 10},
            {'label': 'Top 20 Authors', 'value': 20},
            {'label': 'Top 50 Authors', 'value': 50},
            {'label': 'Top 100 Authors', 'value': 100}
        ],
        value=10,  # Default value
        style={'width': '50%'}
    ),
    dcc.Graph(id='top-authors-gender'),
], id='top-authors'),
    #About
html.Div([
    html.H3('About', style={
        'textAlign': 'center',
        'fontSize': '28px',
        'fontWeight': 'bold',
        'paddingTop': '30px',
        'color': '#2c3e50'  # Dark text for better contrast
    }),
    
    html.P(
        '''This visualization aims to explore the gender diversity trends in computer science (CS) publications over the years.
        It provides insights into the proportion of male, female, and other gendered authors contributing to various CS venues.
        By analyzing historical publication data, this tool helps track progress and identify patterns in gender representation 
        across prominent conferences and journals in the field of computer science.''',
        
        style={
            'textAlign': 'center',
            'fontSize': '18px',
            'lineHeight': '1.6',  # Adjust line height for readability
            'padding': '20px',
            'maxWidth': '800px',
            'margin': 'auto',  # Center the text block
            'color': '#34495e'  # Slightly darker color for the paragraph text
        }
    )
], id='about-cs'),


    # Footer section for contact details and copyright
    html.Div([
        html.Div([
            html.H3('Contact Us'),
            html.P("Email: arunkumarveee@gmail.com"),
        ], style={'textAlign': 'center', 'marginTop': '40px'}),

        html.Div([
            html.P("© 2024 Gender Diversity in CS Publications", style={'textAlign': 'center', 'color': '#777'})
        ], style={'marginTop': '20px'})
    ], style={'position': 'relative', 'bottom': '0', 'width': '100%', 'backgroundColor': '#f7f7f7', 'padding': '10px'})
])



@app.callback(
    Output('overall-gender-dist', 'figure'),
    [Input('home', 'n_clicks')]
)
def render_overall_gender_distribution(n_clicks):
    # Step 1: Calculate gender counts and percentages
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    
    # Calculate total and percentages
    total_authors = gender_counts['Count'].sum()
    gender_counts['Percentage'] = (gender_counts['Count'] / total_authors) * 100
    
    # Debug: Print the DataFrame to check the calculations
    #print(gender_counts)  # This will print the 'gender_counts' DataFrame to the terminal or console
    
    # Step 2: Create the figure without using Plotly Express
    fig = go.Figure()

    # Loop through each gender and add as a separate trace
    for i, row in gender_counts.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Gender']],
            y=[row['Count']],
            name=row['Gender'],
            text=f"{row['Percentage']:.2f}%",  # Display count and percentage
            textposition='outside',
            hovertemplate=f"<b>{row['Gender']}</b><br>Percentage: {row['Percentage']:.2f}%",
            marker_color=color_map.get(row['Gender'], 'gray')  # Use color map
        ))
    
    # Update layout
    fig.update_layout(
        title='Overall Gender Distribution in CS Publications',
        xaxis_title='Gender',
        yaxis_title='Number of Authors',
        hovermode="x unified"
    )
    
    return fig

# Callback to populate the "Gender Distribution Over the Years" visualization
# Dropdown for selecting a conference in "Gender Distribution Over the Years"
@app.callback(
    Output('dropdown-venue', 'options'),
    [Input('home', 'n_clicks')]
)
def update_dropdown_options(n_clicks):
    venue_options = [{'label': re.sub(r'[^\w\s]', '', str(venue)), 'value': venue} for venue in df['Venue'].dropna().unique()]
    return venue_options

# Callback to display the gender distribution over the years based on the selected venue
@app.callback(
    Output('gender-dist-years', 'figure'),
    [Input('dropdown-venue', 'value')]
)
def update_gender_distribution_years(selected_venue):
    if not selected_venue:
        return go.Figure()

    selected_data = df[df['Venue'] == selected_venue]

    if selected_data.empty:
        return go.Figure()

    # Process gender trends over the years for the selected venue
    gender_trends = selected_data.groupby(['Year', 'Gender']).size().reset_index(name='Count')

    # Calculate total authors for each year to compute percentage
    total_authors_per_year = gender_trends.groupby('Year')['Count'].sum().reset_index(name='Total')

    # Merge total authors back with the gender trends
    gender_trends = gender_trends.merge(total_authors_per_year, on='Year')

    # Calculate percentage for each gender
    gender_trends['Percentage'] = (gender_trends['Count'] / gender_trends['Total']) * 100

    fig = go.Figure()

    # Plotting trends for each gender
    for gender in ['male', 'female', 'unisex', 'unknown']:
        gender_data = gender_trends[gender_trends['Gender'] == gender]
        fig.add_trace(go.Scatter(
            x=gender_data['Year'],
            y=gender_data['Percentage'],  # Use percentage for y-axis
            mode='lines+markers',
            name=gender.capitalize(),
            line_shape='linear',
            line=dict(color=color_map.get(gender, 'gray')),
            marker=dict(size=8, line=dict(width=2)),
            hovertemplate="%{y:.2f}%"  # Correct format for hover data
        ))


    fig.update_layout(
        title=f'Gender Distribution by Year for {selected_venue}',
        xaxis_title='Year',
        yaxis_title='Percentage of Authors',
        hovermode="x unified"
    )

    return fig


@app.callback(
    Output('popularity-gender-dist', 'figure'),
    [Input('home', 'n_clicks')]
)
def update_popularity_vs_female(n_clicks):
    # Group by venue and gender to calculate total publications and female percentage
    gender_group = df.groupby(['Venue', 'Gender']).size().reset_index(name='Count')

    # Calculate total publications per venue
    total_publications = gender_group.groupby('Venue')['Count'].sum().reset_index(name='TotalPublications')

    # Merge the total publications with the gender group
    gender_group = gender_group.merge(total_publications, on='Venue')

    # Filter only female authors
    female_group = gender_group[gender_group['Gender'] == 'female']

    # Calculate the female percentage
    female_group = female_group.copy()
    female_group['FemalePercentage'] = (female_group['Count'] / female_group['TotalPublications']) * 100


    # Exclude conferences with fewer than 500 total publications to reduce clustering around 0
    female_group = female_group[female_group['TotalPublications'] >= 500]

    # Create the plot with log scale for the x-axis and hover for labels
    fig = px.scatter(
        female_group,
        x='TotalPublications',
        y='FemalePercentage',
        log_x=True,  # Apply log scale to the x-axis
        size='TotalPublications',  # Adjust marker size based on total publications
        size_max=20,  # Set maximum marker size
        color='FemalePercentage',  # Color by female percentage for visual distinction
        hover_name='Venue',  # Show the conference name on hover instead of as text
        title="Conference Popularity vs Female Author Percentage",
        labels={'TotalPublications': 'Total Publications', 'FemalePercentage': 'Percentage of Female Authors'}
    )

    # Remove text labels and adjust hover template
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey'), opacity=0.7),
                      hovertemplate='<b>%{hovertext}</b><br>Total Publications: %{x}<br>Female Percentage: %{y:.2f}%<extra></extra>')

    fig.update_layout(
        xaxis_title='Total Publications (Log Scale)',
        yaxis_title='Percentage of Female Authors',
        hovermode="closest"
    )

    return fig



# Callback to populate the "Top Authors by Gender" visualization
# Callback to update the graph based on the number of authors selected
@app.callback(
    Output('top-authors-gender', 'figure'),
    [Input('num-authors-dropdown', 'value')]
)
def render_top_authors_by_gender(num_authors):
    # Create a new DataFrame to avoid the warning
    top_authors_gender = df.groupby(['Author_Name', 'Gender']).size().reset_index(name='Number of Publications')

    # Sort values and select top authors based on user input
    top_authors_gender = top_authors_gender.sort_values(by='Number of Publications', ascending=False).head(num_authors)

    # Ensure we're modifying the DataFrame correctly using .loc
    total_publications = top_authors_gender['Number of Publications'].sum()
    top_authors_gender.loc[:, 'Percentage'] = (top_authors_gender['Number of Publications'] / total_publications) * 100

    # Create the bar plot visualization
    fig = px.bar(
        top_authors_gender,
        x='Author_Name',
        y='Number of Publications',
        color='Gender',
        title=f"Top {num_authors} Authors by Gender",
        color_discrete_map=color_map
    )

    # Add percentages to the hover information
    fig.update_traces(
        hovertemplate='<b>Author: %{x}</b><br>Publication: %{y}<br>Percentage: %{customdata:.2f}%',
        customdata=top_authors_gender['Percentage']
    )

    # Update layout for readability
    fig.update_layout(
        xaxis_title="Author",
        yaxis_title="Number of Publications",
        hovermode="x unified",
        xaxis_tickangle=-45,  # Rotate x-axis labels for readability
        height=500
    )
    
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))