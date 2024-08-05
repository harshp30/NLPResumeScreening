from resume_screening import screen_resume
from feedback import get_feedback_on_resume

def main():
    while True:
        # Get user input for resume and job category
        RESUME_PATH = input("Enter your resume path: ")
        JOB_CATEGORY = input("Enter the job category [ml, robotics, hr]: ")
        
        # Screen the resume and display match percentage
        match_percentage = screen_resume(RESUME_PATH, JOB_CATEGORY)
        print(f"Resume match percentage: {match_percentage:.2f}%")

        # Ask for feedback
        FEEDBACK_REQUEST = input("Would you like feedback on how to improve your resume for the role? [Y/N]: ")
        
        if FEEDBACK_REQUEST.lower() in ['y', 'yes']:
            job_description_path = f"/Users/harsh/Desktop/NLPResumeScreening/job_description/{JOB_CATEGORY}.txt"
            feedback = get_feedback_on_resume(RESUME_PATH, job_description_path, JOB_CATEGORY)
            print("\nFeedback on your resume:\n")
            print(feedback)
        else:
            print("Thank you for using the resume screening tool!")

        # Ask if the user wants to compare the resume for a different job category
        REPEAT_REQUEST = input("Would you like to compare your resume for a different job category? [Y/N]: ")
        
        if REPEAT_REQUEST.lower() not in ['y', 'yes']:
            print("Thank you for using the resume screening tool!")
            break

if __name__ == "__main__":
    main()
