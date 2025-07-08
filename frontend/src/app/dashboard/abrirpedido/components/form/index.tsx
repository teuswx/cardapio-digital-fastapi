"use client"
import { Button } from '@/app/dashboard/components/button'
import styles from './styles.module.scss'
import { toast } from 'sonner'
import { getCookieClient } from '@/lib/cookieClient'
import { api } from '@/services/api'
import { useRouter } from 'next/navigation'

export function Form() {
    const router = useRouter()

    async function handleNewOrder(formData: FormData) {
        const table = formData.get("table")
        const name = formData.get("name")

        if (!table || !name) {
            toast.warning("Preencha todos os campos!")
            return;
        }

        const token = getCookieClient();

        console.log(token)

        const data = {
            table: table,
            name: name
        }

        try {
            await api.post("/order/create", data, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            toast.success("Pedido aberto com sucesso!")
        } catch (err) {
            console.log(err)
            toast.warning("Falha ao abrir o pedido!")
            return;
        }

        router.push('/dashboard')

    }

    return (
        <main className={styles.container}>

            <h1>Novo pedido</h1>

            <form
                className={styles.form}
                action={handleNewOrder}
            >
                <input
                    type='number'
                    name='table'
                    placeholder='Digite o número da mesa'
                    required
                    className={styles.input}
                />
                <input
                    type='text'
                    name='name'
                    placeholder='Digite o nome do cliente'
                    required
                    className={styles.input}
                />
                <Button name="Criar" />
            </form>
        </main>
    )
}