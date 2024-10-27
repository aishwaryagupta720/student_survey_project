html_template = '''<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 80%;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .header img {
            width: 100%;  /* Adjust as necessary */
            height: auto;
            display: block;
            margin: auto;
            padding: 10px 0;
        }
        .button {
            display: block;
            width: 200px;
            margin: 20px auto;
            padding: 10px;
            text-align: center;
            background-color: #0056b3;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .footer {
            background-color: #f1f1f1;
            color: #333333;
            text-align: center;
            padding: 10px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://cri-organization-logos.s3.us-east-1.amazonaws.com/general/report.png" alt="CAREER READINESS INVENTORY">
        </div>
        <p>Hi {{student_first_name}},</p>
        <p>Thank you for taking time to reflect on the skills employers value the most. Here is a copy of your report for download:</p>
        <a href="{{report_link}}" class="button">Career Readiness<sup>®</sup> Inventory Report</a>
        <p>Thank you,</p>
        <div class="footer">
            <img src="https://cri-organization-logos.s3.us-east-1.amazonaws.com/general/career-launch.png" alt="Career Launch logo" style="height: 50px;"/>
            <p>in partnership with </p>
            <img src="https://cri-organization-logos.s3.us-east-1.amazonaws.com/general/nace.png" alt="Career Launch logo" style="height: 50px;"/>
        </div>
    </div>
</body>
</html>
'''