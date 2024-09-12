import dash
from dash import dcc, html
from dash.dependencies import Input, Output  # Import Input and Output for callbacks
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# Load your dataset
df = pd.read_csv(r'C:\Users\arunk\OneDrive\Desktop\pro_dash\Cleaned_dataset_gender_visualization.csv')

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
                })
    ]),

    # Navigation buttons aligned horizontally below title with curved edges and no border
    html.Div([
        html.Button('Home', id='home', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'  # No border, curved edges
        }),
        html.Button('Overall Gender Distribution', id='overall', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        }),
        html.Button('Gender Distribution Over the Years', id='years', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        }),
        html.Button('Popularity vs Gender Diversity', id='popularity', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        }),
        html.Button('Top Authors by Gender', id='top_authors', n_clicks=0, style={
            'backgroundColor': '#3498db', 'color': 'white', 'marginRight': '10px', 'padding': '10px 20px',
            'border': 'none', 'borderRadius': '20px'
        })
    ], style={'textAlign': 'center', 'margin': '20px 0'}),

    # Overall Gender Distribution visualization
    html.Div([
        html.H2('Overall Gender Distribution in CS Publications', style={'textAlign': 'center'}),
        dcc.Graph(id='overall-gender-dist', figure={}),
    ]),

    # Gender Distribution Over the Years visualization
    html.Div([
        html.H2('Gender Distribution Over the Years', style={'textAlign': 'center'}),
        # Dropdown for selecting a conference for "Gender Distribution Over the Years"
        dcc.Dropdown(
            id='dropdown-venue',
            placeholder="Select a Conference",
            value=None,
            style={'width': '60%', 'margin': '20px auto'}
        ),
        # Graph for gender distribution over the years
        dcc.Graph(id='gender-dist-years'),
    ]),

    # Popularity vs Gender Diversity visualization
    html.Div([
        html.H2('Conference Popularity vs Gender Diversity', style={'textAlign': 'center'}),
        dcc.Graph(id='popularity-gender-dist', figure={}),
    ]),

    # Top Authors by Gender visualization
    html.Div([
        html.H2('Top Authors by Gender', style={'textAlign': 'center'}),
        dcc.Graph(id='top-authors-gender', figure={}),
    ]),

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
], style={
    'backgroundImage': r'url("C:\Users\arunk\OneDrive\Desktop\pro_dash\assets\gender_diversity_background.jpg")',  # Path to your image in the assets folder
    'backgroundSize': 'cover',  # Ensures the image covers the whole page
    'backgroundAttachment': 'fixed',  # Keeps the background fixed while scrolling
    'height': '100vh',  # Full height to cover the whole page
    'width': '100%'  # Full width
})


# Callback to populate the "Overall Gender Distribution" visualization
@app.callback(
    Output('overall-gender-dist', 'figure'),
    [Input('home', 'n_clicks')]
)
def render_overall_gender_distribution(n_clicks):
    # Overall Gender Distribution
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    
    # Calculate total and percentages
    total_authors = gender_counts['Count'].sum()
    gender_counts['Percentage'] = (gender_counts['Count'] / total_authors) * 100
    
    
    fig = px.bar(
        gender_counts,
        x='Gender',
        y='Count',
        color='Gender',
        color_discrete_map=color_map,
        title='Overall Gender Distribution in CS Publications'
    )
    
    # Customize hover template to include percentage
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Count: %{y:.0f}<br>Percentage: %{customdata[0]:.2f}%',
        customdata=gender_counts[['Percentage']].values,  # Pass the percentage as custom data
        texttemplate='%{y:.0f}',  # Show count on the bar
        textposition='outside'
    )
    
    fig.update_layout(
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
    fig = go.Figure()

    # Plotting trends for each gender
    for gender in ['male', 'female', 'unisex', 'unknown']:
        gender_data = gender_trends[gender_trends['Gender'] == gender]
        fig.add_trace(go.Scatter(
            x=gender_data['Year'],
            y=gender_data['Count'],
            mode='lines+markers',
            name=gender.capitalize(),
            line_shape='linear',
            line=dict(color=color_map.get(gender, 'gray')),
            marker=dict(size=8, line=dict(width=2))
        ))

    fig.update_layout(
        title=f'Gender Distribution by Year for {selected_venue}',
        xaxis_title='Year',
        yaxis_title='Number of Authors',
        hovermode="x unified"
    )
    return fig


# Callback to populate the "Conference Popularity vs Gender Diversity" visualization
@app.callback(
    Output('popularity-gender-dist', 'figure'),
    [Input('home', 'n_clicks')]
)
def render_popularity_vs_gender_diversity(n_clicks):
    # Calculate the number of publications and percentage of female authors for each venue
    conference_gender = df.groupby('Venue').agg(
        total_publications=('Title', 'size'),
        female_authors=('Gender', lambda x: (x == 'female').sum())
    ).reset_index()

    conference_gender['female_percentage'] = (conference_gender['female_authors'] / conference_gender['total_publications']) * 100

    # Scatter plot
    fig = px.scatter(conference_gender, x='total_publications', y='female_percentage', hover_name='Venue',
                     title='Conference Popularity vs Female Author Percentage',
                     labels={'total_publications': 'Total Publications', 'female_percentage': 'Percentage of Female Authors'})
    return fig


# Callback to populate the "Top Authors by Gender" visualization
@app.callback(
    Output('top-authors-gender', 'figure'),
    [Input('home', 'n_clicks')]
)
def render_top_authors_by_gender(n_clicks):
    # Top Authors by Gender
    top_authors_gender = df.groupby(['Author_Name', 'Gender']).size().reset_index(name='Number of Publications')
    top_authors_gender = top_authors_gender.sort_values(by='Number of Publications', ascending=False).head(10)

    fig = px.bar(
        top_authors_gender,
        x='Author_Name',
        y='Number of Publications',
        color='Gender',
        title="Top 10 Authors by Gender",
        text='Number of Publications',
        color_discrete_map=color_map
    )
    fig.update_layout(
        xaxis_title="Author",
        yaxis_title="Number of Publications",
        hovermode="x unified",
        height=500
    )
    return fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)