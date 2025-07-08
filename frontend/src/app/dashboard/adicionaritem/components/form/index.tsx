'use client'

import { Button } from '@/app/dashboard/components/button';
import styles from './styles.module.scss'
import { toast } from 'sonner';
import { getCookieClient } from '@/lib/cookieClient';
import { api } from '@/services/api';
import { useRouter } from 'next/navigation';
interface OrderProps {
    id: number;
    name: string;
    status: boolean;
    table: string;
}

interface ProductProps {
    id: number;
    name: string;
}

interface Props {
    orders: OrderProps[];
    products: ProductProps[];
}

export function Form({ orders, products }: Props) {
    const router = useRouter()

    async function handleAddItem(formData: FormData) {
        const order_id = formData.get("table")
        const product_id = formData.get("product")
        const amount = formData.get("amount")

        if(!order_id || !product_id || !amount){
            toast.warning("Preencha os campos corretamente!")
        }

        const token = getCookieClient()

        const data = {
            order_id: order_id,
            product_id: product_id,
            amount: amount
        }
        console.log(order_id, product_id, amount)
        try{
            await api.post("/order/add",data, {
                headers:{
                    Authorization: `Bearer ${token}`
                }
            })

        }catch(err){
            console.log(err)
            toast.warning("Falha ao adicionar item!")
            return;
        }

        router.push("/dashboard")
        
    }
    return (
        <main className={styles.container}>
            <h1>Adicionar Produto</h1>

            <form className={styles.form} action={handleAddItem}>
                <select name="table">
                    
                    {orders.map((order) => (
                        <option key={order.id} value={order.id}>
                            {order.table}
                        </option>
                    ))}
                </select>

                <select name="product">
                    {products.map((product) => (
                        <option key={product.id} value={product.id}>
                            {product.name}
                        </option>
                    ))}
                </select>

                <input
                    type='number'
                    name='amount'
                    placeholder='Digite a quantidade de items...'
                    required
                    className={styles.input}
                />

                <Button name='Adicionar'/>
            </form>
        </main>

    );
}
