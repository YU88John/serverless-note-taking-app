document.addEventListener('DOMContentLoaded', function () {
    loadNotes();
});

function saveNote() {
    const title = document.getElementById('noteTitle').value;
    const content = document.getElementById('noteContent').value;

    if (title && content) {
        const note = {
            Name: title,
            Content: content
        };

        // Make an HTTP POST request to your API Gateway endpoint
        fetch('https://mrbuwtbz05.execute-api.us-east-1.amazonaws.com/prod/notes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(note),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Note saved successfully:', data);
            // Reload the notes
            loadNotes();
        })
        .catch(error => {
            console.error('Error saving note:', error);
        });

        // Clear the form
        document.getElementById('noteTitle').value = '';
        document.getElementById('noteContent').value = '';
    } else {
        alert('Please enter both title and content');
    }
}

function loadNotes() {
    const noteList = document.getElementById('noteList');
    noteList.innerHTML = ''; // Clear previous notes

    // Make an HTTP GET request to your API Gateway endpoint
    fetch('https://mrbuwtbz05.execute-api.us-east-1.amazonaws.com/prod/notes')
        .then(response => response.json())
        .then(notes => {
            notes.forEach(note => {
                const li = document.createElement('li');
                li.innerHTML = `<h3>${note.Name}</h3><p>${note.Content}</p>`;
                noteList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching notes:', error);
        });
}
