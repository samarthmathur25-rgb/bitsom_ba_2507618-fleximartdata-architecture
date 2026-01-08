Section A: Limitations of RDBMS

Relational databases rely on a rigid, predefined schema, which creates several bottlenecks for a diverse catalog like FlexiMart’s:

Attribute Diversity: In an RDBMS, adding products with distinct attributes (e.g., "RAM" for electronics vs. "Fabric" for apparel) usually requires a "sparse table" with many NULL columns or a complex EAV (Entity-Attribute-Value) model. Both approaches degrade performance and complicate queries.

Schema Rigidity: Every time FlexiMart introduces a new product category, an ALTER TABLE command is required. In large production environments, this can cause significant downtime and requires careful migration planning.

Impedance Mismatch: Storing customer reviews in an RDBMS requires a separate Reviews table linked by foreign keys. Retrieving a product with its reviews necessitates expensive JOIN operations, which slow down the application as the dataset grows.

Section B: NoSQL Benefits

MongoDB’s document-oriented architecture is purpose-built for the flexibility FlexiMart requires:

Flexible Schema (BSON Documents): MongoDB stores data as documents. One document can have 10 fields while the next has 5. This allows "Laptops" and "Shoes" to coexist in the same Products collection, each containing only relevant fields without the need for NULL values.

Embedded Documents: Instead of joining tables, customer reviews can be stored as an array of objects directly inside the product document. This allows the application to fetch a product and all its reviews in a single, high-speed read operation.

Horizontal Scalability: Unlike RDBMS, which usually scales "up" (bigger servers), MongoDB scales "out" through sharding. It can distribute data across multiple commodity servers, making it easier and more cost-effective to handle millions of products and high traffic.

Section C: Trade-offs

While MongoDB offers agility, it involves specific trade-offs:

Data Redundancy and Storage: Since MongoDB encourages embedding (denormalization), data like "Category Names" or "Vendor Details" might be repeated across many documents. This increases storage requirements compared to the normalized structure of MySQL.

Lack of Complex Joins: MongoDB is not designed for heavy relational lifting. If FlexiMart needs to perform complex multi-collection reporting (e.g., cross-referencing inventory, shipping, and tax tables in one query), the logic must be handled in the application code, which can be more difficult to maintain than a standard SQL JOIN.