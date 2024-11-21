:- use_module(library(http/http_server)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_json)).
:- use_module(library(http/http_files)).
:- use_module(library(csv)).

% Dynamic student predicate to hold CSV data
:- dynamic student/3.

% Load data from CSV file
:- initialization(load_data).

load_data :-
    csv_read_file('student.csv', Rows, [functor(student), arity(3)]),
    % Remove the header row if present
    exclude(is_header_row, Rows, DataRows),
    maplist(assert, DataRows).

% Helper predicate to detect and skip the header row
is_header_row(student('student_id', 'attendance_percentage', 'cgpa')).

% REST API Handlers
:- http_handler(root(eligibility), check_eligibility, []).
:- http_handler(root(debar), check_exam_permission, []).

% Static file handler for serving HTML and other assets
:- http_handler(root(.), http_reply_from_files('./static', []), [prefix]).

% Check scholarship eligibility
check_eligibility(Request) :-
    http_read_json_dict(Request, Dict),
    Student_ID = Dict.student_id,
    ( eligible_for_scholarship(Student_ID) ->
        Reply = _{student_id: Student_ID, scholarship_eligible: true}
    ; Reply = _{student_id: Student_ID, scholarship_eligible: false} ),
    reply_json_dict(Reply).

% Check exam permission
check_exam_permission(Request) :-
    http_read_json_dict(Request, Dict),
    Student_ID = Dict.student_id,
    ( permitted_for_exam(Student_ID) ->
        Reply = _{student_id: Student_ID, exam_permitted: true}
    ; Reply = _{student_id: Student_ID, exam_permitted: false} ),
    reply_json_dict(Reply).

% Scholarship eligibility rule
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance_Percentage, CGPA),
    number(Attendance_Percentage), number(CGPA), % Ensure numeric comparison
    Attendance_Percentage >= 75,
    CGPA >= 9.0.

% Exam permission rule
permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance_Percentage, _),
    number(Attendance_Percentage), % Ensure numeric comparison
    Attendance_Percentage >= 75.

% Start the server
:- initialization(http_server(http_dispatch, [port(8080)])).
