import { Orders } from "./components/orders";
import {api} from '@/services/api'
import { getCookieServer  } from "@/lib/cookieServer";
import { OrderProps } from "@/lib/order.type";

async function getOrders(): Promise<OrderProps[] | []>{

    const token = await getCookieServer();

    try{
        const response = await api.get("/order/list", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })

        return response.data || []
    }catch(err){
        console.log(err)
        return []
    }
}
export default async function Dashboard(){

    const orders = await getOrders();

    
    return(
        <>
            <Orders orders={orders}/>
        </>
    )
}