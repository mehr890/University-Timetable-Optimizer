# 🎓 University Timetable Optimizer

An **ML-based University Timetable Optimizer** that generates and evaluates personalized university timetables based on student preferences and scheduling constraints.

## 📌 Project Overview

University students often face timetable problems such as unwanted class timings, classes on inconvenient days, long gaps between classes, and scheduling conflicts.

This project uses **Machine Learning and timetable optimization techniques** to evaluate different schedule arrangements and identify a timetable that better matches the student's preferences.

The application provides an interactive **Streamlit web interface** where users can explore the timetable and view the optimized schedule.

## ✨ Features

* 📅 Generate and display university timetables
* 🤖 Machine Learning-based timetable evaluation
* 🎯 Personalized timetable scoring
* ⚠️ Detect timetable clashes
* 📊 Analyze classes per day
* 🕐 Consider class timings and late classes
* 📉 Penalize unwanted gaps between classes
* 👍 Consider preferred days
* 🚫 Consider avoided days
* 📈 Timetable visualization
* 🌐 Interactive Streamlit interface

## 🧠 Machine Learning Component

The ML component is used to predict the suitability/rating of timetable arrangements.

The system considers scheduling-related features such as:

* Day of the week
* Class timing
* Preferred days
* Avoided days
* Late classes
* Gaps between classes
* Number of classes per day
* Timetable conflicts

The predicted rating is combined with personalized scheduling criteria to help identify a more suitable timetable.

## 🏗️ Project Structure

```text
university-timetable-optimizer/
│
├── app.py
├── cleaned_timetable.csv
├── model.pkl
├── requirements.txt
└── README.md
```

### Files

| File                    | Description                          |
| ----------------------- | ------------------------------------ |
| `app.py`                | Main Streamlit application           |
| `cleaned_timetable.csv` | Cleaned university timetable dataset |
| `model.pkl`             | Trained Machine Learning model       |
| `requirements.txt`      | Required Python libraries            |
| `README.md`             | Project documentation                |

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Joblib**
* **Streamlit**
* **Matplotlib / Plotly** *(if used in the application)*

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/university-timetable-optimizer.git
```

Navigate to the project folder:

```bash
cd university-timetable-optimizer
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 📊 Workflow

```text
University Timetable Dataset
          ↓
     Data Cleaning
          ↓
 Feature Preparation
          ↓
 Machine Learning Model
          ↓
 Timetable Evaluation
          ↓
 Personalized Scoring
          ↓
 Optimized Timetable
          ↓
 Streamlit Visualization
```

## 🎯 Objective

The main objective of this project is to demonstrate how **Machine Learning can be integrated with timetable optimization** to create personalized and user-friendly university schedules.

Instead of simply generating a timetable, the system evaluates schedules according to individual preferences and attempts to produce a timetable with:

* Fewer conflicts
* Better preferred-day alignment
* Fewer unwanted late classes
* More suitable class distribution
* Reduced unnecessary gaps
* Higher personalized suitability

## 🌐 Streamlit Application

The project can be deployed as an interactive web application using **Streamlit Cloud**.

Users can interact with the application without running the Python code locally.

## 🚀 Future Improvements

Possible future improvements include:

* 👤 Multiple student profiles
* 🧑‍🏫 Teacher availability constraints
* 🏫 Room availability optimization
* 🔄 Automatic timetable generation
* 🧬 Genetic Algorithm optimization
* 🤖 More advanced ML models
* 📱 Improved responsive interface
* 💾 Export timetable to PDF/Excel
* 🔐 User accounts and saved preferences

## 👩‍💻 Author

**Mehreen Naz**

BS Computer Science | Data Science & Machine Learning

---

⭐ If you find this project useful, consider giving the repository a **star**.
