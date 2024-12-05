from django.shortcuts import render, redirect
from .models import Stock
import yfinance as yf
from django.views.decorators.csrf import csrf_exempt

def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        return round(current_price, 2)
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def index(request):
    stocks = Stock.objects.all()
    portfolio_data = []
    total_value = 0

    for stock in stocks:
        current_price = get_stock_price(stock.ticker)
        if current_price:
            value = current_price * stock.quantity
            profit_loss = (current_price - stock.purchase_price) * stock.quantity
            percentage_change = ((current_price - stock.purchase_price) / stock.purchase_price) * 100

            portfolio_data.append({
                'ticker': stock.ticker,
                'quantity': stock.quantity,
                'purchase_price': stock.purchase_price,
                'current_price': current_price,
                'value': round(value, 2),
                'profit_loss': round(profit_loss, 2),
                'percentage_change': round(percentage_change, 2),
            })
            total_value += value

    return render(request, 'portfolio/index.html', {
        'portfolio_data': portfolio_data,
        'total_value': round(total_value, 2),
    })






def search_stock(request):
    stock_data = None
    if request.method == "GET":
        # Check for dropdown selection or custom ticker input
        stock_name = request.GET.get('stock_name')
        custom_stock_name = request.GET.get('custom_stock_name')

        # Determine which stock to use, giving priority to dropdown selection
        query = stock_name if stock_name else custom_stock_name

        if query:
            try:
                stock = yf.Ticker(query)
                info = stock.history(period="1d")
                if not info.empty:
                    stock_data = {
                        'ticker': query.upper(),
                        'current_price': round(info['Close'].iloc[-1], 2),
                    }
                else:
                    stock_data = {'error': f"No data found for {query}"}
            except Exception as e:
                print(f"Error fetching data for {query}: {e}")
                stock_data = {'error': f"Error fetching data for {query}"}

    return render(request, 'portfolio/search_stock.html', {'stock_data': stock_data})



@csrf_exempt
def add_stock(request):
    if request.method == "POST":
        ticker = request.POST.get('ticker')
        purchase_price = float(request.POST.get('current_price'))
        quantity = 1  # Default quantity; can be updated later.

        try:
            # Check if the stock already exists in the portfolio
            stock = Stock.objects.get(ticker=ticker)
            
            # If the stock exists, update the quantity and purchase price if needed
            stock.quantity += 1  # Increment quantity by 1; adjust logic if needed
            stock.purchase_price = purchase_price  # Update purchase price if necessary
            stock.save()  # Save the changes to the database

        except Stock.DoesNotExist:
            # If the stock does not exist, create a new stock entry
            Stock.objects.create(ticker=ticker, purchase_price=purchase_price, quantity=quantity)

        return redirect('index')





def delete_stock(request, ticker):
    Stock.objects.filter(ticker=ticker).delete()
    return redirect('index')
