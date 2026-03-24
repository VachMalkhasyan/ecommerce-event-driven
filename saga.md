# Choreography-based Saga

## What is a Saga?
A Saga is a design pattern used to manage data consistency across multiple microservices in a distributed system by breaking a long-running transaction into a series of smaller, local transactions. Each local transaction updates the database and publishes an event or message to trigger the next local transaction in the saga. If a local transaction fails, the saga executes a series of compensating transactions that undo the changes made by the preceding local transactions.

## Why Choreography?
Choreography was chosen over orchestration for this project because it promotes loose coupling between services, as there is no central "orchestrator" directing the flow. Each service independently listens for events and decides which action to take, making the system more resilient and easier to scale without a single point of failure. This approach is well-suited for the early stages of this e-commerce system where the business logic is still evolving.

## Failure Flow (Payment Failed)
1. **Order Service**: Publishes `OrderCreated` event.
2. **Payment Service**: Consumes `OrderCreated`, attempts payment processing, and fails (30% mock failure rate).
3. **Payment Service**: Publishes `PaymentFailed` event.
4. **Order Service**: Consumes `PaymentFailed` (Saga participant).
5. **Order Service**: Updates the internal order status to `CANCELLED`.
6. **Order Service**: Publishes `OrderCancelled` compensating event to notify other services (e.g., to release inventory if it was already reserved).
