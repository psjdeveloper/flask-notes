from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# -------------------------
# Database Setup
# -------------------------
def init_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# -------------------------
# Home Page - Show Notes
# -------------------------
@app.route('/')
def index():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Notes App</title>
        <style>
            body { font-family: Arial; background-color: #f3f4f6; padding: 20px; }
            .note { background: white; padding: 15px; border-radius: 8px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            a { text-decoration: none; color: #2563eb; }
            .add { background: #2563eb; color: white; padding: 10px 15px; border-radius: 6px; }
            .delete { color: red; }
        </style>
    </head>
    <body>
        <h1>📝 My Notes</h1>
        <a class="add" href="/add">Add New Note</a>
        <hr>
        {% for note in notes %}
            <div class="note">
                <h3>{{ note[1] }}</h3>
                <p>{{ note[2] }}</p>
                <a class="delete" href="/delete/{{ note[0] }}">Delete</a>
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, notes=notes)

# -------------------------
# Add New Note Page
# -------------------------
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect("notes.db")
        c = conn.cursor()
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect('/')
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Note</title>
        <style>
            body { font-family: Arial; background-color: #f3f4f6; padding: 20px; }
            form { display: flex; flex-direction: column; max-width: 400px; margin: auto; }
            input, textarea { margin: 10px 0; padding: 10px; border-radius: 6px; border: 1px solid #ccc; }
            button { background: #2563eb; color: white; padding: 10px; border: none; border-radius: 6px; }
        </style>
    </head>
    <body>
        <h2>Add a New Note</h2>
        <form method="POST">
            <input type="text" name="title" placeholder="Note title" required>
            <textarea name="content" placeholder="Write something..." required></textarea>
            <button type="submit">Save</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

# -------------------------
# Delete Note
# -------------------------
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
