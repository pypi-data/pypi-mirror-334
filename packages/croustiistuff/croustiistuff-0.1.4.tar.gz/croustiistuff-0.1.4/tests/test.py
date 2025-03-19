import time
from Croustiistuff import Solver

cap = Solver(capsolver_api_key="CAP-8802DD695EAA8AB84037FCC393DB2EE9")

def testSolve():
    start_time = time.perf_counter()  # Start timer

    capkey = cap.RecaptchaV2("https://www.google.com/recaptcha/api2/demo", "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-")

    end_time = time.perf_counter()  # End timer
    elapsed_time = end_time - start_time  # Calculate duration

    print(f"CAPTCHA Key: {capkey}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    testSolve()
