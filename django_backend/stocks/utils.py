import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering
import matplotlib.pyplot as plt
import io
import base64
from datetime import timedelta

def generate_stock_plot(dates, actual_prices, predicted_prices):
    # Ensure there is data to plot
    if len(dates) == 0 or len(actual_prices) == 0:
        raise ValueError("No data available to generate the plot.")

    plt.figure(figsize=(10, 6))
    
    # Plot actual prices for the first 200 days
    plt.plot(dates, actual_prices, label='Actual Prices', color='blue')

    # Get the last date from the actual data using .iloc
    last_date = dates.iloc[-1]  # Correct way to access the last date in Pandas

    # Extend the dates to include the next 30 days for predicted prices
    future_dates = [last_date + timedelta(days=i+1) for i in range(len(predicted_prices))]

    # Plot predicted prices for the next 30 days
    plt.plot(future_dates, predicted_prices, label='Predicted Prices', color='red', linestyle='--')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title('Actual vs Predicted Stock Prices')
    plt.legend()

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert plot to base64 string
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # Close the plot to free up memory
    plt.close()

    return img_base64

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import base64
from PIL import Image
from reportlab.lib.utils import ImageReader

def generate_pdf_report(metrics, img_base64):
    """
    Generate a PDF report with stock metrics and a base64-encoded image plot.

    :param metrics: A dictionary containing key financial metrics like total return, max drawdown, etc.
    :param img_base64: A base64 string representation of the image (plot).
    :return: A BytesIO object representing the generated PDF.
    """
    # Create a BytesIO buffer to store the PDF
    buffer = io.BytesIO()
    
    # Create a PDF canvas
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 50, "Stock Performance Report")
    
    # Financial Metrics
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 100, "Key Financial Metrics:")
    c.drawString(40, height - 120, f"Total Return: {metrics['total_return']}%")
    c.drawString(40, height - 140, f"Max Drawdown: {metrics['max_drawdown']}%")
    c.drawString(40, height - 160, f"Number of Trades: {metrics['trades_executed']}")
    
    # Decode the base64 image and add it to the PDF
    img_data = base64.b64decode(img_base64)
    
    # Use PIL to open the image from the decoded data
    image = Image.open(io.BytesIO(img_data))
    reportlab_image = ImageReader(image)

    # Draw the image in the PDF
    c.drawImage(reportlab_image, 30, height - 400, width=500, height=300)
    
    # Finalize and save the PDF
    c.showPage()
    c.save()
    
    # Return the PDF buffer (BytesIO)
    buffer.seek(0)
    return buffer