"use client";
import styles from './styles.module.scss';
import { X } from 'lucide-react';
import { useContext } from 'react';  // Corrigido: `use` não é correto aqui
import { OrderContext } from '@/providers/order';
import { calculateTotalOrder } from '@/lib/helper';

export function Modalorder() {
    const { onRequestClose, order, finishOrder } = useContext(OrderContext);  // Usando useContext para obter os dados do contexto

    console.log("aqui", order)
    // Verifica se o pedido não está carregado
    if (!order) {
        return <div>Carregando...</div>;  // Exibe um indicador de carregamento enquanto os dados do pedido não estão disponíveis
    }

    async function handleFinishOrder() {
         if (order) {
            await finishOrder(order.id);  // Usa `order.id` pois `order` agora é um único objeto
        }  
    }

    return (
        <dialog className={styles.dialogContainer}>
            <section className={styles.dialogContent}>
                <button className={styles.dialogBack} onClick={onRequestClose}>
                    <X size={40} color='#FF3f4b' />
                </button>

                <article className={styles.container}>
                    <h2>Detalhes do pedido</h2>

                    <span className={styles.table}>
                        Mesa <b>{order.order.table}</b>
                    </span>

                    {order.order.name && (
                        <span className={styles.name}>
                            <b>{order.order.name}</b>
                        </span>
                    )}

                    {/* Exibe os itens do pedido */}
                    <section className={styles.item} key={order.id}>
                        <span>Qtd: {order.amount} - <b>{order.product.name}</b> - R$    {Number(order.product.price) * Number(order.amount)}</span>
                        <span className={styles.description}>{order.product.description}</span>
                    </section>

                    <h3 className={styles.total}>Valor total do pedido: R$ {calculateTotalOrder([order])}</h3>

                    <button className={styles.buttonOrder} onClick={handleFinishOrder}>
                        Concluir pedido
                    </button>
                </article>
            </section>
        </dialog>
    );
}
