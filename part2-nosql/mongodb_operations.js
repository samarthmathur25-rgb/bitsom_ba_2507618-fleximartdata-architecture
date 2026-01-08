// Connect to the FlexiMart database
use('FlexiMartDB');

// ==========================================
// Operation 1: Load Data
// ==========================================
// Note: If using the VS Code MongoDB Extension, you can right-click your 
// products_catalog.json file and select "Import to MongoDB". 
// Below is the script command to insert the data provided:

const catalogData = [ /* Paste the full JSON array here */ ];
db.products.insertMany(catalogData);
console.log("Data loaded successfully.");


// ==========================================
// Operation 2: Basic Query
// ==========================================
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
db.products.find(
  { 
    category: "Electronics", 
    price: { $lt: 50000 } 
  },
  { 
    name: 1, 
    price: 1, 
    stock: 1, 
    _id: 0 
  }
);


// ==========================================
// Operation 3: Review Analysis
// ==========================================
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array
db.products.aggregate([
  {
    $addFields: {
      avgRating: { $avg: "$reviews.rating" }
    }
  },
  {
    $match: {
      avgRating: { $gte: 4.0 }
    }
  }
]);


// ==========================================
// Operation 4: Update Operation
// ==========================================
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}
db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user_id: "U999", // Adjusted key to match your sample data 'user_id'
        rating: 4,
        comment: "Good value",
        date: new ISODate()
      }
    }
  }
);


// ==========================================
// Operation 5: Complex Aggregation
// ==========================================
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      avg_price: 1,
      product_count: 1
    }
  },
  {
    $sort: { avg_price: -1 }
  }
]);