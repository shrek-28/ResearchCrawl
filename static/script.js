// Function to show the README content in a dialog box
function showReadme(content) {
    document.getElementById('readmeContent').textContent = content;
    document.getElementById('dialogOverlay').style.display = 'flex';
}

// Function to close the dialog box
function closeDialog() {
    document.getElementById('dialogOverlay').style.display = 'none';
}