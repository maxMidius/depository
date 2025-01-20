import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dash import Dash, html, dcc, dash_table, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models.faq_models import Base, QuestionGroup, Question, Tag, Answer
from dash import callback_context as ctx

# Database setup
engine = create_engine('sqlite:///faq.db')
Session = sessionmaker(bind=engine)

def layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),  # Add URL tracking
        # Add Alert Components
        dbc.Alert(id='success-alert', is_open=False, duration=4000, color="success"),
        dbc.Alert(id='error-alert', is_open=False, duration=4000, color="danger"),
        dbc.Row([
            # Left Panel - Question List
            dbc.Col([
                html.H4("FAQ Questions", className="w3-text-blue-grey"),
                dbc.Button("+ New Question", id="new-question-btn", color="primary", className="mb-3"),
                dash_table.DataTable(
                    id='questions-table',
                    columns=[
                        {'name': 'Q#', 'id': 'question_number'},
                        {'name': 'Question', 'id': 'text'},
                        {'name': 'Group', 'id': 'group_name'}
                    ],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left'}
                )
            ], width=6),
            
            # Right Panel - Editor
            dbc.Col([
                html.H4("Question Editor", className="w3-text-blue-grey"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Question Group"),
                        dcc.Dropdown(id='group-select')
                    ], className="mb-3"),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Question Number"),
                        dbc.Input(id='question-number', type='text', placeholder="A:001")
                    ], className="mb-3"),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Question"),
                        dbc.Textarea(id='question-text')
                    ], className="mb-3"),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Tags"),
                        dcc.Dropdown(id='tags-select', multi=True)
                    ], className="mb-3"),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Answer"),
                        dcc.Textarea(
                            id='answer-text',
                            style={'width': '100%', 'height': 200}
                        )
                    ], className="mb-3"),
                ]),
                
                dbc.Button("Save", id="save-btn", color="success", className="me-2"),
                dbc.Button("Delete", id="delete-btn", color="danger")
            ], width=6)
        ])
    ])

def init_callbacks(app):
    @app.callback(
        [Output('questions-table', 'data'),
         Output('group-select', 'options'),
         Output('tags-select', 'options')],
        Input('url', 'pathname')
    )
    def initialize_data(_):
        session = Session()
        try:
            questions = session.query(Question).all()
            groups = session.query(QuestionGroup).all()
            tags = session.query(Tag).all()
            
            print(f"Found {len(questions)} questions")  # Debug
            
            questions_data = [{
                'question_number': q.question_number,
                'text': q.text,
                'group_name': q.group.name if q.group else ''
            } for q in questions]
            
            group_options = [{'label': g.name, 'value': g.id} for g in groups]
            tag_options = [{'label': t.name, 'value': t.id} for t in tags]
            
            return questions_data, group_options, tag_options
        finally:
            session.close()

    @app.callback(
        [Output('group-select', 'value'),
         Output('question-number', 'value'),
         Output('question-text', 'value'),
         Output('tags-select', 'value'),
         Output('answer-text', 'value')],
        Input('questions-table', 'active_cell'),
        State('questions-table', 'data')
    )
    def load_selected_question(active_cell, table_data):
        if not active_cell:
            return no_update, no_update, no_update, no_update, no_update
            
        row_idx = active_cell['row']
        selected_q_number = table_data[row_idx]['question_number']
        print(f"Selected question: {selected_q_number}")  # Debug
        
        session = Session()
        try:
            question = session.query(Question).filter_by(
                question_number=selected_q_number
            ).first()
            
            if question:
                print(f"Loading question: {question.text}")  # Debug
                return (
                    question.group_id,
                    question.question_number,
                    question.text,
                    [tag.id for tag in question.tags],
                    question.answer.html_content if question.answer else ''
                )
            return no_update, no_update, no_update, no_update, no_update
        finally:
            session.close()

    def generate_question_number(session, group_id):
        # Get group prefix (A, B, C etc based on group)
        group = session.query(QuestionGroup).filter_by(id=group_id).first()
        prefix = chr(64 + group.id) if group else 'A'  # A for group 1, B for 2 etc
        
        # Get highest number for this prefix
        last_question = session.query(Question)\
            .filter(Question.question_number.like(f'{prefix}:%'))\
            .order_by(Question.question_number.desc())\
            .first()
        
        if last_question:
            last_num = int(last_question.question_number.split(':')[1])
            new_num = last_num + 1
        else:
            new_num = 1
            
        return f"{prefix}:{new_num:03d}"

    @app.callback(
        [Output('group-select', 'value', allow_duplicate=True),
         Output('question-number', 'value', allow_duplicate=True),
         Output('question-text', 'value', allow_duplicate=True),
         Output('tags-select', 'value', allow_duplicate=True),
         Output('answer-text', 'value', allow_duplicate=True)],
        Input('new-question-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def clear_form_for_new_question(n_clicks):
        if n_clicks:
            # Clear all form fields
            return [
                None,  # group select
                '',    # question number (will be auto-generated on save)
                '',    # question text
                [],    # tags
                ''     # answer
            ]
        return [no_update] * 5

    # Question selection and form handling
    @app.callback(
        [Output('questions-table', 'data', allow_duplicate=True),
         Output('group-select', 'value', allow_duplicate=True),
         Output('question-number', 'value', allow_duplicate=True),
         Output('question-text', 'value', allow_duplicate=True),
         Output('tags-select', 'value', allow_duplicate=True),
         Output('answer-text', 'value', allow_duplicate=True),
         Output('success-alert', 'children'),
         Output('success-alert', 'is_open'),
         Output('error-alert', 'children'),
         Output('error-alert', 'is_open')],
        [Input('save-btn', 'n_clicks'),
         Input('new-question-btn', 'n_clicks'),
         Input('questions-table', 'active_cell')],
        [State('group-select', 'value'),
         State('question-number', 'value'),
         State('question-text', 'value'),
         State('answer-text', 'value'),
         State('tags-select', 'value'),
         State('questions-table', 'data')],
        prevent_initial_call=True
    )
    def handle_form_events(save_clicks, new_clicks, active_cell,
                         group_id, question_number, question_text,
                         answer_text, tag_ids, table_data):
        ctx_msg = ctx.triggered[0]
        trigger_id = ctx_msg['prop_id'].split('.')[0]
        session = Session()
        question = None  # Define question at function scope

        try:
            # Handle New Question
            if trigger_id == 'new-question-btn':
                print("Creating new question form")
                return [table_data, None, '', '', [], '', '', False, '', False]

            # Handle Save
            elif trigger_id == 'save-btn':
                print(f"Save attempt - Group: {group_id}, Text: {question_text}")

                if not group_id:
                    return [no_update] * 6 + ['', False, 'Please select a Question Group', True]
                if not question_text or not question_text.strip():
                    return [no_update] * 6 + ['', False, 'Please enter Question Text', True]

                # Generate or use existing question number
                if not question_number:
                    question_number = generate_question_number(session, group_id)
                    print(f"Generated new question number: {question_number}")
                    question = Question(
                        group_id=group_id,
                        question_number=question_number,
                        text=question_text.strip()
                    )
                    session.add(question)
                else:
                    question = session.query(Question).filter_by(
                        question_number=question_number
                    ).first()
                    if question:
                        question.group_id = group_id
                        question.text = question_text.strip()
                    else:
                        # Handle case where question_number exists but question not found
                        question = Question(
                            group_id=group_id,
                            question_number=question_number,
                            text=question_text.strip()
                        )
                        session.add(question)

                # Save question first to ensure it exists
                session.flush()

                # Handle answer
                if answer_text and answer_text.strip():
                    if not question.answer:
                        answer = Answer(
                            question=question,
                            html_content=answer_text.strip()
                        )
                        session.add(answer)
                    else:
                        question.answer.html_content = answer_text.strip()

                # Handle tags
                if tag_ids:
                    tags = session.query(Tag).filter(Tag.id.in_(tag_ids)).all()
                    question.tags = tags

                session.commit()
                print(f"Successfully saved question {question_number}")

                # Refresh table
                questions = session.query(Question).all()
                questions_data = [{
                    'question_number': q.question_number,
                    'text': q.text,
                    'group_name': q.group.name if q.group else ''
                } for q in questions]

                success_msg = f"Successfully saved question {question_number}"
                return [questions_data, None, '', '', [], '', success_msg, True, '', False]

            # Handle Question Selection
            elif trigger_id == 'questions-table' and active_cell:
                row_idx = active_cell['row']
                selected_q_number = table_data[row_idx]['question_number']
                question = session.query(Question).filter_by(
                    question_number=selected_q_number
                ).first()

                if question:
                    return [
                        table_data,
                        question.group_id,
                        question.question_number,
                        question.text,
                        [tag.id for tag in question.tags],
                        question.answer.html_content if question.answer else '',
                        '', False, '', False
                    ]

            return [no_update] * 6 + ['', False, '', False]

        except Exception as e:
            print(f"Error in form handling: {str(e)}")
            session.rollback()
            return [no_update] * 6 + ['', False, str(e), True]

        finally:
            session.close()

        return [no_update] * 10

    @app.callback(
        [Output('questions-table', 'data', allow_duplicate=True),
         Output('group-select', 'value', allow_duplicate=True),
         Output('question-number', 'value', allow_duplicate=True),
         Output('question-text', 'value', allow_duplicate=True),
         Output('tags-select', 'value', allow_duplicate=True),
         Output('answer-text', 'value', allow_duplicate=True)],
        Input('delete-btn', 'n_clicks'),
        [State('question-number', 'value'),
         State('questions-table', 'data')],
        prevent_initial_call=True
    )
    def delete_question(n_clicks, question_number, table_data):
        if not n_clicks or not question_number:
            return [no_update] * 6
            
        session = Session()
        try:
            # Find and delete the question
            question = session.query(Question).filter_by(
                question_number=question_number
            ).first()
            
            if question:
                session.delete(question)
                session.commit()
                
                # Refresh questions table
                questions = session.query(Question).all()
                questions_data = [{
                    'question_number': q.question_number,
                    'text': q.text,
                    'group_name': q.group.name if q.group else ''
                } for q in questions]
                
                # Clear form
                return [questions_data, None, '', '', [], '']
                
        except Exception as e:
            print(f"Error deleting question: {e}")
            session.rollback()
            return [no_update] * 6
            
        finally:
            session.close()
            
        return [no_update] * 6

if __name__ == '__main__':
    app = Dash(__name__, 
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://www.w3schools.com/w3css/4/w3.css"
        ],
        suppress_callback_exceptions=True  # Add this line
    )
    app.layout = layout()
    init_callbacks(app)
    app.run_server(debug=True, port=8055)