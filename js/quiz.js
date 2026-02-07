// Quiz System for HTML, CSS, and JavaScript Learning
class QuizSystem {
    constructor() {
        this.currentCategory = null;
        this.questions = [];
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.userAnswers = [];
        this.quizData = this.loadQuizData();

        this.init();
    }

    init() {
        // DOM Elements
        this.categorySelection = document.getElementById('category-selection');
        this.quizInterface = document.getElementById('quiz-interface');
        this.quizResults = document.getElementById('quiz-results');
        this.questionText = document.getElementById('question-text');
        this.optionsContainer = document.getElementById('options');
        this.feedback = document.getElementById('feedback');
        this.progressFill = document.getElementById('progress-fill');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.retryBtn = document.getElementById('retry-btn');
        this.backToCategoriesBtn = document.getElementById('back-to-categories');

        // Event Listeners
        this.categorySelection.addEventListener('click', (e) => {
            const categoryCard = e.target.closest('.category-card');
            if (categoryCard) {
                this.startQuiz(categoryCard.dataset.category);
            }
        });

        this.optionsContainer.addEventListener('click', (e) => {
            const option = e.target.closest('.option');
            if (option && !option.classList.contains('selected')) {
                this.selectOption(option);
            }
        });

        this.prevBtn.addEventListener('click', () => this.previousQuestion());
        this.nextBtn.addEventListener('click', () => this.nextQuestion());
        this.retryBtn.addEventListener('click', () => this.retryQuiz());
        this.backToCategoriesBtn.addEventListener('click', () => this.backToCategories());

        // Load saved progress
        this.loadProgress();
    }

    loadQuizData() {
        return {
            html: {
                beginner: [
                    {
                        question: "Apa singkatan dari HTML?",
                        options: ["HyperText Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlink and Text Markup Language"],
                        correct: 0,
                        explanation: "HTML adalah singkatan dari HyperText Markup Language, bahasa markup standar untuk membuat halaman web."
                    },
                    {
                        question: "Tag HTML mana yang digunakan untuk heading utama?",
                        options: ["<p>", "<h1>", "<div>", "<span>"],
                        correct: 1,
                        explanation: "<h1> adalah tag untuk heading utama, yang paling penting dalam hierarki heading."
                    },
                    {
                        question: "Atribut mana yang digunakan untuk memberikan ID unik pada elemen HTML?",
                        options: ["class", "id", "name", "type"],
                        correct: 1,
                        explanation: "Atribut 'id' memberikan identifikasi unik pada elemen HTML."
                    },
                    {
                        question: "Tag HTML mana yang digunakan untuk membuat paragraf?",
                        options: ["<br>", "<p>", "<hr>", "<div>"],
                        correct: 1,
                        explanation: "Tag <p> digunakan untuk membuat paragraf teks."
                    },
                    {
                        question: "Apa fungsi dari tag <a> dalam HTML?",
                        options: ["Membuat gambar", "Membuat link", "Membuat tabel", "Membuat form"],
                        correct: 1,
                        explanation: "Tag <a> digunakan untuk membuat hyperlink atau link ke halaman lain."
                    }
                ],
                intermediate: [
                    {
                        question: "Atribut 'target' pada tag <a> dengan nilai '_blank' akan...",
                        options: ["Membuka link di tab yang sama", "Membuka link di tab baru", "Menutup browser", "Menyegarkan halaman"],
                        correct: 1,
                        explanation: "target='_blank' membuka link di tab atau jendela browser baru."
                    },
                    {
                        question: "Elemen HTML5 mana yang digunakan untuk navigasi?",
                        options: ["<nav>", "<menu>", "<navigate>", "<navigation>"],
                        correct: 0,
                        explanation: "<nav> adalah elemen semantik HTML5 untuk area navigasi."
                    },
                    {
                        question: "Tag HTML mana yang digunakan untuk membuat tabel?",
                        options: ["<table>", "<tab>", "<tbl>", "<grid>"],
                        correct: 0,
                        explanation: "<table> adalah tag utama untuk membuat tabel di HTML."
                    },
                    {
                        question: "Atribut 'alt' pada tag <img> berfungsi untuk...",
                        options: ["Mengubah ukuran gambar", "Memberikan teks alternatif", "Mengubah format gambar", "Menambah border"],
                        correct: 1,
                        explanation: "Atribut alt memberikan teks alternatif untuk gambar jika gambar tidak dapat dimuat."
                    },
                    {
                        question: "Form method mana yang mengirim data melalui URL?",
                        options: ["POST", "GET", "PUT", "DELETE"],
                        correct: 1,
                        explanation: "Method GET mengirim data melalui URL (query string)."
                    }
                ],
                advanced: [
                    {
                        question: "Elemen HTML5 mana yang digunakan untuk konten yang tidak terkait dengan dokumen utama?",
                        options: ["<aside>", "<article>", "<section>", "<main>"],
                        correct: 0,
                        explanation: "<aside> digunakan untuk konten yang secara tidak langsung terkait dengan konten utama."
                    },
                    {
                        question: "Atribut 'data-*' dalam HTML5 digunakan untuk...",
                        options: ["Menyimpan data khusus", "Mengubah style", "Membuat animasi", "Mengatur layout"],
                        correct: 0,
                        explanation: "Atribut data-* memungkinkan penyimpanan data khusus pada elemen HTML."
                    },
                    {
                        question: "Tag <meta> dengan name='viewport' digunakan untuk...",
                        options: ["SEO", "Responsive design", "Analytics", "Social media"],
                        correct: 1,
                        explanation: "Meta viewport mengontrol layout pada perangkat mobile untuk responsive design."
                    },
                    {
                        question: "Elemen <canvas> HTML5 digunakan untuk...",
                        options: ["Video", "Audio", "Grafik 2D/3D", "Database"],
                        correct: 2,
                        explanation: "<canvas> menyediakan area untuk menggambar grafik menggunakan JavaScript."
                    },
                    {
                        question: "Atribut 'autocomplete' pada form input digunakan untuk...",
                        options: ["Validasi", "Styling", "Autofill browser", "Encryption"],
                        correct: 2,
                        explanation: "autocomplete membantu browser mengisi form secara otomatis."
                    }
                ]
            },
            css: {
                beginner: [
                    {
                        question: "Properti CSS mana yang digunakan untuk mengubah warna teks?",
                        options: ["color", "background-color", "text-color", "font-color"],
                        correct: 0,
                        explanation: "Properti 'color' mengubah warna teks elemen HTML."
                    },
                    {
                        question: "Selector CSS mana yang memilih semua elemen <p>?",
                        options: [".p", "#p", "p", "paragraph"],
                        correct: 2,
                        explanation: "Selector 'p' memilih semua elemen paragraf."
                    },
                    {
                        question: "Properti CSS untuk mengubah ukuran font adalah...",
                        options: ["font-size", "text-size", "size", "font"],
                        correct: 0,
                        explanation: "font-size mengatur ukuran huruf."
                    },
                    {
                        question: "Nilai properti display 'none' akan...",
                        options: ["Menyembunyikan elemen", "Menampilkan elemen", "Mengubah ukuran", "Mengubah warna"],
                        correct: 0,
                        explanation: "display: none menyembunyikan elemen dari tampilan."
                    },
                    {
                        question: "Properti CSS untuk memberikan margin di semua sisi adalah...",
                        options: ["margin", "padding", "border", "spacing"],
                        correct: 0,
                        explanation: "margin mengatur ruang di luar elemen."
                    }
                ],
                intermediate: [
                    {
                        question: "Properti CSS Flexbox mana yang mengatur arah item?",
                        options: ["flex-direction", "flex-wrap", "justify-content", "align-items"],
                        correct: 0,
                        explanation: "flex-direction mengatur arah (row/column) dari flex items."
                    },
                    {
                        question: "Selector CSS ':hover' digunakan untuk...",
                        options: ["Elemen saat diklik", "Elemen saat di-hover", "Elemen saat difokus", "Elemen saat aktif"],
                        correct: 1,
                        explanation: ":hover memilih elemen saat kursor mouse berada di atasnya."
                    },
                    {
                        question: "Properti CSS Grid 'grid-template-columns' digunakan untuk...",
                        options: ["Mengatur baris", "Mengatur kolom", "Mengatur gap", "Mengatur area"],
                        correct: 1,
                        explanation: "grid-template-columns mendefinisikan kolom dalam CSS Grid."
                    },
                    {
                        question: "Unit CSS 'rem' relatif terhadap...",
                        options: ["Viewport", "Parent element", "Root element", "Current element"],
                        correct: 2,
                        explanation: "rem relatif terhadap ukuran font root element (biasanya <html>)."
                    },
                    {
                        question: "Properti CSS 'position: absolute' mengatur posisi relatif terhadap...",
                        options: ["Viewport", "Parent terdekat dengan position", "Elemen sebelumnya", "Elemen berikutnya"],
                        correct: 1,
                        explanation: "position: absolute relatif terhadap parent terdekat yang memiliki position selain static."
                    }
                ],
                advanced: [
                    {
                        question: "Fungsi CSS calc() digunakan untuk...",
                        options: ["Animasi", "Perhitungan matematika", "Transformasi", "Gradient"],
                        correct: 1,
                        explanation: "calc() memungkinkan perhitungan matematika dalam nilai CSS."
                    },
                    {
                        question: "@media query dalam CSS digunakan untuk...",
                        options: ["Animasi", "Responsive design", "Typography", "Color scheme"],
                        correct: 1,
                        explanation: "@media query membuat style responsif berdasarkan ukuran layar."
                    },
                    {
                        question: "Properti CSS 'z-index' mengatur...",
                        options: ["Ukuran elemen", "Posisi stacking", "Transparansi", "Border radius"],
                        correct: 1,
                        explanation: "z-index mengontrol urutan stacking elemen yang overlap."
                    },
                    {
                        question: "CSS Custom Properties (variabel) dideklarasikan dengan...",
                        options: ["--nama-variabel", "$nama-variabel", "@nama-variabel", "#nama-variabel"],
                        correct: 0,
                        explanation: "Custom properties CSS menggunakan sintaks --nama-variabel."
                    },
                    {
                        question: "Properti CSS 'clip-path' digunakan untuk...",
                        options: ["Shadow", "Border", "Cropping shape", "Animation"],
                        correct: 2,
                        explanation: "clip-path membuat bentuk cropping yang kompleks pada elemen."
                    }
                ]
            },
            javascript: {
                beginner: [
                    {
                        question: "Keyword JavaScript mana yang digunakan untuk mendeklarasikan variabel yang bisa diubah?",
                        options: ["const", "let", "var", "static"],
                        correct: 1,
                        explanation: "'let' mendeklarasikan variabel yang bisa diubah nilainya."
                    },
                    {
                        question: "Operator JavaScript untuk membandingkan nilai dan tipe data adalah...",
                        options: ["==", "===", "!=", "!=="],
                        correct: 1,
                        explanation: "=== membandingkan baik nilai maupun tipe data (strict equality)."
                    },
                    {
                        question: "Method JavaScript untuk menampilkan pesan di console adalah...",
                        options: ["alert()", "print()", "console.log()", "display()"],
                        correct: 2,
                        explanation: "console.log() menampilkan pesan di developer console."
                    },
                    {
                        question: "Tipe data JavaScript mana yang menyimpan true/false?",
                        options: ["string", "number", "boolean", "array"],
                        correct: 2,
                        explanation: "Boolean menyimpan nilai true atau false."
                    },
                    {
                        question: "Struktur kontrol JavaScript untuk menjalankan kode berdasarkan kondisi adalah...",
                        options: ["for", "while", "if", "switch"],
                        correct: 2,
                        explanation: "if statement menjalankan kode jika kondisi terpenuhi."
                    }
                ],
                intermediate: [
                    {
                        question: "Method array JavaScript untuk menambah elemen di akhir array adalah...",
                        options: ["push()", "pop()", "shift()", "unshift()"],
                        correct: 0,
                        explanation: "push() menambah satu atau lebih elemen di akhir array."
                    },
                    {
                        question: "Fungsi JavaScript setTimeout() digunakan untuk...",
                        options: ["Loop", "Conditional", "Delay eksekusi", "Error handling"],
                        correct: 2,
                        explanation: "setTimeout() menunda eksekusi kode selama waktu tertentu."
                    },
                    {
                        question: "DOM method untuk memilih elemen berdasarkan ID adalah...",
                        options: ["getElementById()", "getElementsByClassName()", "querySelector()", "getElementsByTagName()"],
                        correct: 0,
                        explanation: "getElementById() memilih elemen tunggal berdasarkan atribut id."
                    },
                    {
                        question: "Event listener JavaScript 'click' dipicu ketika...",
                        options: ["Mouse hover", "Mouse click", "Key press", "Page load"],
                        correct: 1,
                        explanation: "Event 'click' terjadi saat elemen diklik dengan mouse."
                    },
                    {
                        question: "Operator JavaScript '&&' adalah operator...",
                        options: ["OR", "AND", "NOT", "XOR"],
                        correct: 1,
                        explanation: "&& adalah logical AND operator."
                    }
                ],
                advanced: [
                    {
                        question: "ES6 feature untuk template literal menggunakan...",
                        options: ["''", "\"\"", "``", "//"],
                        correct: 2,
                        explanation: "Template literal menggunakan backticks (`) dan memungkinkan interpolasi."
                    },
                    {
                        question: "Method JavaScript untuk mengubah array menjadi string adalah...",
                        options: ["split()", "join()", "concat()", "slice()"],
                        correct: 1,
                        explanation: "join() menggabungkan elemen array menjadi string."
                    },
                    {
                        question: "Promise dalam JavaScript menangani...",
                        options: ["Error", "Async operations", "Loop", "DOM manipulation"],
                        correct: 1,
                        explanation: "Promise menangani operasi asynchronous seperti API calls."
                    },
                    {
                        question: "Arrow function ES6 ditulis dengan sintaks...",
                        options: ["function() {}", "() => {}", "=> () {}", "-> () {}"],
                        correct: 1,
                        explanation: "() => {}" adalah sintaks arrow function."
                    },
                    {
                        question: "Local storage menyimpan data sebagai...",
                        options: ["Objects", "Strings", "Numbers", "Arrays"],
                        correct: 1,
                        explanation: "Local storage hanya menyimpan data sebagai string."
                    }
                ]
            }
        };
    }

    startQuiz(category) {
        this.currentCategory = category;
        this.questions = this.getQuestionsForCategory(category);
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.userAnswers = [];

        this.categorySelection.classList.add('hidden');
        this.quizInterface.classList.remove('hidden');
        this.quizResults.classList.add('hidden');

        this.showQuestion();
        this.updateProgress();
        this.updateButtons();
    }

    getQuestionsForCategory(category) {
        const levels = ['beginner', 'intermediate', 'advanced'];
        let allQuestions = [];

        levels.forEach(level => {
            if (this.quizData[category] && this.quizData[category][level]) {
                allQuestions = allQuestions.concat(
                    this.quizData[category][level].map(q => ({ ...q, level }))
                );
            }
        });

        // Shuffle questions
        return this.shuffleArray(allQuestions);
    }

    showQuestion() {
        const question = this.questions[this.currentQuestionIndex];
        this.questionText.innerHTML = `<strong>${question.level.charAt(0).toUpperCase() + question.level.slice(1)}:</strong> ${question.question}`;

        this.optionsContainer.innerHTML = '';
        question.options.forEach((option, index) => {
            const optionElement = document.createElement('div');
            optionElement.className = 'option';
            optionElement.dataset.index = index;
            optionElement.innerHTML = option;
            this.optionsContainer.appendChild(optionElement);
        });

        this.feedback.classList.add('hidden');

        // Show previous answer if exists
        if (this.userAnswers[this.currentQuestionIndex] !== undefined) {
            const selectedOption = this.optionsContainer.children[this.userAnswers[this.currentQuestionIndex]];
            selectedOption.classList.add('selected');
            this.showFeedback();
        }
    }

    selectOption(optionElement) {
        // Remove previous selection
        const options = this.optionsContainer.children;
        for (let opt of options) {
            opt.classList.remove('selected');
        }

        // Select new option
        optionElement.classList.add('selected');
        const selectedIndex = parseInt(optionElement.dataset.index);
        this.userAnswers[this.currentQuestionIndex] = selectedIndex;

        this.showFeedback();
    }

    showFeedback() {
        const question = this.questions[this.currentQuestionIndex];
        const selectedAnswer = this.userAnswers[this.currentQuestionIndex];
        const feedback = this.feedback;

        feedback.classList.remove('hidden');

        if (selectedAnswer === question.correct) {
            feedback.className = 'feedback correct';
            feedback.innerHTML = '<strong>✅ Benar!</strong>';
            if (!this.userAnswers.includes(selectedAnswer)) {
                this.score++;
            }
        } else {
            feedback.className = 'feedback incorrect';
            feedback.innerHTML = '<strong>❌ Salah!</strong>';
        }

        feedback.innerHTML += `<div class="explanation">${question.explanation}</div>`;

        // Highlight correct answer
        const options = this.optionsContainer.children;
        options[question.correct].classList.add('correct');
        if (selectedAnswer !== question.correct) {
            options[selectedAnswer].classList.add('incorrect');
        }
    }

    nextQuestion() {
        if (this.currentQuestionIndex < this.questions.length - 1) {
            this.currentQuestionIndex++;
            this.showQuestion();
            this.updateProgress();
            this.updateButtons();
        } else {
            this.showResults();
        }
    }

    previousQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            this.showQuestion();
            this.updateProgress();
            this.updateButtons();
        }
    }

    updateProgress() {
        const progress = ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
        this.progressFill.style.width = `${progress}%`;
    }

    updateButtons() {
        this.prevBtn.disabled = this.currentQuestionIndex === 0;
        this.nextBtn.textContent = this.currentQuestionIndex === this.questions.length - 1 ? 'Selesai' : 'Selanjutnya';
    }

    showResults() {
        this.quizInterface.classList.add('hidden');
        this.quizResults.classList.remove('hidden');

        const totalQuestions = this.questions.length;
        const correctAnswers = this.score;
        const incorrectAnswers = totalQuestions - correctAnswers;
        const percentage = Math.round((correctAnswers / totalQuestions) * 100);

        document.getElementById('final-score').textContent = `${correctAnswers}/${totalQuestions}`;
        document.getElementById('correct-answers').textContent = correctAnswers;
        document.getElementById('incorrect-answers').textContent = incorrectAnswers;
        document.getElementById('total-questions').textContent = totalQuestions;
        document.getElementById('score-percentage').textContent = `${percentage}%`;

        const scoreMessage = document.getElementById('score-message');
        const scoreDescription = document.getElementById('score-description');

        if (percentage >= 80) {
            scoreMessage.textContent = '🎉 Luar Biasa!';
            scoreDescription.textContent = 'Anda memiliki pemahaman yang sangat baik tentang materi ini.';
        } else if (percentage >= 60) {
            scoreMessage.textContent = '👍 Bagus!';
            scoreDescription.textContent = 'Anda memiliki pemahaman yang baik, tapi masih bisa ditingkatkan.';
        } else if (percentage >= 40) {
            scoreMessage.textContent = '📚 Perlu Belajar Lagi';
            scoreDescription.textContent = 'Anda perlu mempelajari materi ini lebih dalam.';
        } else {
            scoreMessage.textContent = '💪 Jangan Menyerah!';
            scoreDescription.textContent = 'Teruslah belajar dan coba lagi untuk meningkatkan pemahaman Anda.';
        }

        // Save progress
        this.saveProgress();
    }

    retryQuiz() {
        this.startQuiz(this.currentCategory);
    }

    backToCategories() {
        this.quizResults.classList.add('hidden');
        this.categorySelection.classList.remove('hidden');
    }

    saveProgress() {
        const progress = {
            category: this.currentCategory,
            score: this.score,
            totalQuestions: this.questions.length,
            date: new Date().toISOString(),
            answers: this.userAnswers
        };

        localStorage.setItem('quizProgress', JSON.stringify(progress));
    }

    loadProgress() {
        const saved = localStorage.getItem('quizProgress');
        if (saved) {
            const progress = JSON.parse(saved);
            // Could display last score or resume quiz
            console.log('Previous quiz progress:', progress);
        }
    }

    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }
}

// Initialize quiz system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new QuizSystem();
});
