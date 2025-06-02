// Personal Task Manager JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize task checkboxes
    initializeTaskCheckboxes();

    // Initialize form validation
    initializeFormValidation();

    // Initialize tooltips
    initializeTooltips();
});

function initializeTaskCheckboxes() {
    const checkboxes = document.querySelectorAll('.task-checkbox');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            const isChecked = this.checked;

            // Add loading state
            const taskCard = this.closest('.task-card');
            taskCard.classList.add('loading');

            // Send AJAX request to toggle task
            toggleTask(taskId, isChecked, taskCard, this);
        });
    });
}

function toggleTask(taskId, isChecked, taskCard, checkbox) {
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/toggle/${taskId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            completed: isChecked
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update UI based on completion status
            updateTaskUI(taskCard, data.completed);

            // Show success message
            showNotification(
                data.completed ? 'Task marked as completed!' : 'Task marked as pending!',
                'success'
            );

            // Update statistics (if on task list page)
            updateTaskStatistics();
        } else {
            // Revert checkbox state on error
            checkbox.checked = !isChecked;
            showNotification('Error updating task. Please try again.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Revert checkbox state on error
        checkbox.checked = !isChecked;
        showNotification('Network error. Please check your connection.', 'error');
    })
    .finally(() => {
        // Remove loading state
        taskCard.classList.remove('loading');
    });
}

function updateTaskUI(taskCard, completed) {
    const title = taskCard.querySelector('.card-title');
    const badge = taskCard.querySelector('.badge');

    if (completed) {
        taskCard.classList.add('completed-task');
        title.classList.add('text-decoration-line-through', 'text-muted');
        badge.className = 'badge bg-success';
        badge.textContent = 'Completed';
    } else {
        taskCard.classList.remove('completed-task');
        title.classList.remove('text-decoration-line-through', 'text-muted');
        badge.className = 'badge bg-warning';
        badge.textContent = 'Pending';
    }
}

function updateTaskStatistics() {
    // Count current pending and completed tasks
    const pendingTasks = document.querySelectorAll('.task-card:not(.completed-task)').length;
    const completedTasks = document.querySelectorAll('.task-card.completed-task').length;

    // Update statistics display
    const pendingCountElements = document.querySelectorAll('.text-warning');
    const completedCountElements = document.querySelectorAll('.text-success');

    pendingCountElements.forEach(el => {
        if (el.tagName === 'H3') {
            el.textContent = pendingTasks;
        }
    });

    completedCountElements.forEach(el => {
        if (el.tagName === 'H3') {
            el.textContent = completedTasks;
        }
    });

    // Update filter buttons
    const pendingButton = document.querySelector('a[href="?status=pending"]');
    const completedButton = document.querySelector('a[href="?status=completed"]');

    if (pendingButton) {
        pendingButton.textContent = `Pending (${pendingTasks})`;
    }
    if (completedButton) {
        completedButton.textContent = `Completed (${completedTasks})`;
    }
}

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');

                    // Remove invalid class on input
                    field.addEventListener('input', function() {
                        this.classList.remove('is-invalid');
                    });
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields.', 'error');
            }
        });
    });
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Utility function to get CSRF token
function getCSRFToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : '';
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add loading states to buttons
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        }
    });
});

// Auto-hide alerts after 5 seconds
document.querySelectorAll('.alert:not(.alert-dismissible)').forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
});
