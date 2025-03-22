document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap validate karne ke liye
    document.querySelectorAll('.needs-validation').forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Confirm dialog before deleting
    document.querySelectorAll('[data-confirm]').forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm(this.dataset.confirm)) {
                event.preventDefault();
            }
        });
    });

    // Password toggle karne ke liye
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');
    
    if (togglePassword && password) {
        togglePassword.addEventListener('click', function () {
            password.type = password.type === 'password' ? 'text' : 'password';
            this.classList.toggle('bi-eye');
        });
    }

    // chart.js se data fetch karne ke liye
    fetch('/api/student_scores')
        .then(response => response.json())
        .then(data => {
            // Color array for different subjects
            const colors = [
                'rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 
                'rgba(255, 206, 86, 0.5)', 'rgba(75, 192, 192, 0.5)', 
                'rgba(153, 102, 255, 0.5)', 'rgba(255, 159, 64, 0.5)'
            ];

            if (data.student) {
                // student ko dikhnne wala chart
                const studentChart = document.getElementById('studentScoreChart');
                if (!studentChart) {
                    console.error('Student chart score not found');
                    return;
                }

                const scores = data.scores || [];
                if (scores.length === 0) {
                    studentChart.style.display = 'none';
                    console.log('No scores available');
                    return;
                }

                const subjects = [...new Set(scores.map(entry => entry.subject))];
                const datasets = subjects.map((subject, index) => ({
                    label: subject,
                    data: scores.filter(entry => entry.subject === subject).map(entry => entry.score),
                    backgroundColor: colors[index % colors.length],
                    borderColor: colors[index % colors.length].replace('0.5', '1'),
                    borderWidth: 1
                }));

                new Chart(studentChart.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: scores.map(entry => entry.quiz),
                        datasets: datasets
                    },
                    options: { 
                        responsive: true, 
                        scales: { 
                            y: { 
                                beginAtZero: true,
                                max: 100, 
                                title: {
                                    display: true,
                                    text: 'Score (%)'
                                },
                                ticks: {    // percentage sign include karne ke liye y axis mein
                                    callback: function(value) {
                                        return value + '%'; 
                                    }
                                }
                            },
                            x: { // x axis ka title
                                title: {
                                    display: true,
                                    text: 'Quizzes'
                                }
                            }
                        },
                        plugins: {  // zoom and pan karne ke liye
                            tooltip: {  // tooltip mein label ke saath percentage sign include karne ke liye
                                callbacks: {  
                                    label: function(context) {
                                        return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + '%';
                                    }
                                }
                            },
                            title: {   
                                display: true,
                                text: 'Your Scores by Subject (%)'
                            },
                            legend: {
                                display: true,
                                position: 'top'
                            }
                        }
                }
            });
            } else {
                // admin ko dikhnne wala chart
                const adminChart = document.getElementById('adminScoreChart');
                if (!adminChart) {
                    console.error('chart for admin not found');
                    return;
                }
            
                const students = Object.keys(data);
                if (students.length === 0) {
                    adminChart.style.display = 'none';
                    console.log('No student data available');
                    return;
                }
            
                const datasets = students.map((student, index) => ({   // student ke naam ke saath uska score
                    label: student,
                    data: data[student].map(entry => entry.score), 
                    backgroundColor: colors[index % colors.length],
                    borderColor: colors[index % colors.length].replace('0.5', '1'),
                    borderWidth: 1,
                    fill: false
                }));
            
                new Chart(adminChart.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: data[students[0]].map(entry => entry.quiz), // quiz ke naam
                        datasets: datasets
                    },
                    options: { 
                        responsive: true, 
                        scales: { 
                            y: { 
                                beginAtZero: true,
                                max: 100,
                                title: {
                                    display: true,
                                    text: 'Score (%)'
                                },
                                ticks: {
                                    callback: function(value) {
                                        return value.toFixed(1) + '%';
                                    }
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Quizzes'
                                }
                            }
                        },
                        plugins: {
                            zoom: {
                                zoom: {
                                    wheel: {
                                        enabled: true,
                                    },
                                    pinch: {
                                        enabled: true
                                    },
                                    mode: 'y',
                                },
                                pan: {
                                    enabled: true,
                                    mode: 'y',
                                },
                                limits: {
                                    y: {
                                        min: 0,
                                        max: 100
                                    }
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + '%';
                                    }
                                }
                            },
                            title: {
                                display: true,
                                text: 'All Students\' Scores (%)'
                            },
                            legend: {
                                display: true,
                                position: 'top'
                            }
                        }
                    }
                });
            }
            
        })
        .catch(error => console.error('Error fetching scores:', error));
});
