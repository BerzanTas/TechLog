const apiBaseURL = '/api/solutions/';

// Pobieranie elementów DOM
const solutionsContainer = document.getElementById('solutions-container');
const solutionForm = document.getElementById('solution-form');
const titleInput = document.getElementById('title');
const contentInput = document.getElementById('content'); // Zmienione na 'content'

// Funkcja do renderowania listy rozwiązań
const fetchSolutions = async () => {
    try {
        const response = await fetch(apiBaseURL);
        const solutions = await response.json();

        // Wyczyść kontener i renderuj nowe rozwiązania
        solutionsContainer.innerHTML = '';
        solutions.forEach(solution => {
            const solutionElement = document.createElement('div');
            solutionElement.innerHTML = `
                <h2>${solution.title}</h2>
                <p>${solution.content}</p> <!-- Zmienione z 'description' na 'content' -->
                <button onclick="deleteSolution(${solution.id})">Delete</button>
                <button onclick="editSolution(${solution.id}, '${solution.title}', '${solution.content}')">Edit</button>
            `;
            solutionsContainer.appendChild(solutionElement);
        });
    } catch (error) {
        console.error('Error fetching solutions:', error);
    }
};

// Dodawanie nowego rozwiązania
solutionForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const newSolution = {
        title: titleInput.value,
        content: contentInput.value // Zmienione z 'description' na 'content'
    };

    try {
        const response = await fetch(apiBaseURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newSolution)
        });

        if (response.ok) {
            titleInput.value = '';
            contentInput.value = ''; // Zmienione z 'description' na 'content'
            fetchSolutions(); // Odśwież listę
        } else {
            console.error('Error creating solution:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Usuwanie rozwiązania
const deleteSolution = async (id) => {
    try {
        const response = await fetch(`${apiBaseURL}${id}/`, {
            method: 'DELETE'
        });

        if (response.ok) {
            fetchSolutions(); // Odśwież listę
        } else {
            console.error('Error deleting solution:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

// Edytowanie rozwiązania
const editSolution = (id, currentTitle, currentContent) => {
    // Wyświetl dane w formularzu
    titleInput.value = currentTitle;
    contentInput.value = currentContent; // Zmienione z 'description' na 'content'

    // Obsługa edycji po kliknięciu "Save"
    solutionForm.onsubmit = async (event) => {
        event.preventDefault();

        const updatedSolution = {
            title: titleInput.value,
            content: contentInput.value // Zmienione z 'description' na 'content'
        };

        try {
            const response = await fetch(`${apiBaseURL}${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedSolution)
            });

            if (response.ok) {
                titleInput.value = '';
                contentInput.value = ''; // Zmienione z 'description' na 'content'
                fetchSolutions(); // Odśwież listę
                solutionForm.onsubmit = addSolutionHandler; // Przywróć domyślną funkcję
            } else {
                console.error('Error updating solution:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
};

// Domyślna funkcja obsługi formularza (dodawanie)
const addSolutionHandler = async (event) => {
    event.preventDefault();

    const newSolution = {
        title: titleInput.value,
        content: contentInput.value // Zmienione z 'description' na 'content'
    };

    try {
        const response = await fetch(apiBaseURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newSolution)
        });

        if (response.ok) {
            titleInput.value = '';
            contentInput.value = ''; // Zmienione z 'description' na 'content'
            fetchSolutions(); // Odśwież listę
        } else {
            console.error('Error creating solution:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

// Pierwsze załadowanie danych
fetchSolutions();
