import { OrderItemProps } from "@/providers/order";

export function calculateTotalOrder(orders: OrderItemProps[]){
    return orders.reduce((total,item)=>{
        const itemTotal = Number(item.product.price) * Number(item.amount);
        return total+ itemTotal
    }, 0)
}