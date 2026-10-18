# Medium Task: Shopping Cart System

## Objective
Identify and fix defects in cart.py.

Preserve the existing class name, method names,
and parameters.

## Functional Requirements

1. The shopping cart must support adding,
   removing, and listing products.

2. add_item(item, price, quantity) must:
   - Accept nonempty product names.
   - Accept nonnegative numeric prices.
   - Accept positive integer quantities.
   - Raise ValueError for invalid inputs.

3. Adding an existing product:
   - Increases its quantity if the price matches.
   - Raises ValueError if the price differs.
   - Must not modify the item when rejected.

4. remove_item(item) must:
   - Remove the entire product from the cart.
   - Do nothing if the product does not exist.

5. get_subtotal() must:
   - Calculate the sum of price × quantity.
   - Return 0 for an empty cart.

6. get_total(subtotal, percentage) must:
   - Apply the specified percentage discount.
   - Accept percentages from 0 to 100 inclusive.
   - Raise ValueError for invalid percentages.
   - Round the result to two decimal places.

7. list_items() must:
   - Return a list of product names as strings.
   - Preserve insertion order.

8. Products must be stored in a dictionary,
   using product names as keys.

## Constraints

- Preserve class name shopping_cart.
- Preserve existing method names and parameters.
- Do not modify TASK.md.