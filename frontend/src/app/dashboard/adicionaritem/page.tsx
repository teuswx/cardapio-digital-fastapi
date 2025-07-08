import { getCookieServer } from '@/lib/cookieServer'
import {Form} from './components/form'
import { api } from '@/services/api'


export default async function AdicionarItem(){

    const token = await getCookieServer()

    const orders = await api.get("/order/list",{
        headers:{
            Authorization: `Bearer ${token}`
        }
    })

    const products = await api.get("/product/list",{
        headers:{
            Authorization: `Bearer ${token}`
        }
    })

    return(
        <Form orders={orders.data} products={products.data}/>
    )
}