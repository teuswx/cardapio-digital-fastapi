"use client" // Isso indica que o código abaixo é para ser executado no lado do cliente (no navegador).

import { createContext, ReactNode, useState } from 'react' // Importa as funções e tipos necessários para criar um contexto e gerenciar o estado.
import { api } from '@/services/api';
import { getCookieClient } from '@/lib/cookieClient';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';

export interface OrderItemProps {
    id: number;
    amount: number;
    created_at: string;
    order_id: number;
    product_id: number;
    product: {
        id: number;
        name: string;
        price: string;
        description: string;
        banner: string;
        category_id: number;
    };
    order: {
        id: number;
        table: number;
        name: string | null;
        draft: boolean;
        status: boolean;
    }
}

type OrderContextData = {  // Define o tipo de dados que o nosso contexto irá armazenar.
    isOpen: boolean; // Um valor booleano que indica se o pedido está aberto ou fechado.
    onRequestOpen: (order_id: number) => Promise<void>; // Função que será chamada para abrir o pedido.
    onRequestClose: () => void; // Função que será chamada para fechar o pedido.
    order: OrderItemProps[];
    finishOrder: (order_id: number) => Promise<void>;
}

type OrderProviderProps = {  // Define o tipo das propriedades que o "OrderProvider" vai receber.
    children: ReactNode; // Isso permite que outros componentes sejam passados dentro do "OrderProvider".
}

export const OrderContext = createContext({} as OrderContextData)  // Cria um contexto, que é como uma "caixa" para armazenar dados que podemos compartilhar entre vários componentes.

export function OrderProvider({ children }: OrderProviderProps) {  // Este é o componente que vai "fornecer" os dados para os outros componentes (o contexto).

    const [isOpen, setIsOpen] = useState(false) // Cria um estado chamado "isOpen" para armazenar se o pedido está aberto (true) ou fechado (false).
    const [order, setOrder] = useState<OrderItemProps[]>([]);
    const router = useRouter();

    async function onRequestOpen(order_id: number) {  // Função para abrir o pedido.

        const token = getCookieClient();
        try {
            const response = await api.get("/order/detail", {
                headers: {
                    Authorization: `Bearer ${token}`
                },
                params: {
                    order_id: order_id
                }
            })
            setOrder(response.data)
        } catch (err){
            console.log(err)
            toast.error("Não existe items adicionados ao pedido")
            return;
        }

        setIsOpen(true)  // Define o estado "isOpen" como true, indicando que o pedido está aberto.
    }

    function onRequestClose() {  // Função para fechar o pedido.
        setIsOpen(false)  // Define o estado "isOpen" como false, indicando que o pedido está fechado.
    }


    async function finishOrder(order_id: number) {
        console.log(order_id)
        const token = getCookieClient();

        const data = {
            order_id: order_id
        }

        try {
            await api.put("/order/finish", data, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
        } catch (err) {
            console.log(err)
            toast.error("Falha ao finalizar este pedido")
            return;
        }

        toast.success("Pedido finalizado com sucesso!")
        router.refresh();
        setIsOpen(false);
    }



    return (  // Retorna o componente "OrderContext.Provider", que envolve outros componentes e fornece os dados (o contexto) para eles.
        <OrderContext.Provider
            value={{  // O "value" é o que será fornecido para os componentes dentro do "OrderProvider".
                isOpen,  // Passa o estado de "isOpen" (se o pedido está aberto ou fechado).
                onRequestOpen,  // Passa a função para abrir o pedido.
                onRequestClose,  // Passa a função para fechar o pedido.
                finishOrder,
                order
            }}
        >
            {children}  {/*"children" aqui é tudo o que estiver dentro de "OrderProvider" quando for utilizado.*/}
        </OrderContext.Provider>
    )
}
