<script setup>
import { reactive, computed } from 'vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  cartIsEmpty: { type: Boolean, required: true },
})

const emit = defineEmits(['confirm'])

const form = reactive({
  name: '',
  phone: '',
  pickupOption: 'asap', // asap | chosen
  pickupTime: '',
  paymentMethod: '', // 'Pagar en local' | 'Pagar online (demo)'
  note: '',
})

const errors = reactive({
  name: '',
  phone: '',
  paymentMethod: '',
  cart: '',
})

const pickupTimeOptions = ['19:30', '20:00', '20:30', '21:00', '21:30', '22:00']

function validate() {
  errors.name = form.name.trim() ? '' : 'Indica tu nombre.'
  errors.phone = form.phone.trim() ? '' : 'Indica un teléfono de contacto.'
  errors.paymentMethod = form.paymentMethod ? '' : 'Elige un método de pago.'
  errors.cart = props.cartIsEmpty ? 'Tu pedido está vacío.' : ''

  return !errors.name && !errors.phone && !errors.paymentMethod && !errors.cart
}

const resolvedPickupTime = computed(() =>
  form.pickupOption === 'asap' ? 'Lo antes posible' : form.pickupTime || 'Por confirmar',
)

function handleSubmit() {
  if (!validate()) return

  emit('confirm', {
    name: form.name.trim(),
    phone: form.phone.trim(),
    pickupTime: resolvedPickupTime.value,
    paymentMethod: form.paymentMethod,
    note: form.note.trim(),
  })
}
</script>

<template>
  <form class="flex flex-col gap-5" novalidate @submit.prevent="handleSubmit">
    <div v-if="errors.cart" class="bg-brand-red/10 text-brand-red-dark text-sm rounded-xl px-4 py-3">
      {{ errors.cart }}
    </div>

    <div>
      <label class="block text-sm font-semibold text-brand-text mb-1" for="name">Nombre</label>
      <input
        id="name"
        v-model="form.name"
        type="text"
        placeholder="Tu nombre"
        class="w-full rounded-xl border border-brand-border bg-brand-card px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-red"
      />
      <p v-if="errors.name" class="text-brand-red text-sm mt-1">{{ errors.name }}</p>
    </div>

    <div>
      <label class="block text-sm font-semibold text-brand-text mb-1" for="phone">Teléfono</label>
      <input
        id="phone"
        v-model="form.phone"
        type="tel"
        placeholder="600 000 000"
        class="w-full rounded-xl border border-brand-border bg-brand-card px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-red"
      />
      <p v-if="errors.phone" class="text-brand-red text-sm mt-1">{{ errors.phone }}</p>
    </div>

    <div>
      <p class="block text-sm font-semibold text-brand-text mb-2">Hora de recogida</p>
      <div class="flex flex-col gap-2">
        <label
          class="flex items-center gap-3 rounded-xl border px-4 py-3 cursor-pointer transition"
          :class="form.pickupOption === 'asap' ? 'border-brand-red bg-brand-red/5' : 'border-brand-border bg-brand-card'"
        >
          <input v-model="form.pickupOption" type="radio" value="asap" class="accent-brand-red" />
          <span>Lo antes posible</span>
        </label>
        <label
          class="flex items-center gap-3 rounded-xl border px-4 py-3 cursor-pointer transition"
          :class="form.pickupOption === 'chosen' ? 'border-brand-red bg-brand-red/5' : 'border-brand-border bg-brand-card'"
        >
          <input v-model="form.pickupOption" type="radio" value="chosen" class="accent-brand-red" />
          <span>Elegir hora</span>
        </label>
        <select
          v-if="form.pickupOption === 'chosen'"
          v-model="form.pickupTime"
          class="w-full rounded-xl border border-brand-border bg-brand-card px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-red"
        >
          <option value="" disabled>Selecciona una hora</option>
          <option v-for="time in pickupTimeOptions" :key="time" :value="time">{{ time }}</option>
        </select>
      </div>
    </div>

    <div>
      <p class="block text-sm font-semibold text-brand-text mb-2">Método de pago</p>
      <div class="flex flex-col gap-2">
        <label
          class="flex items-center gap-3 rounded-xl border px-4 py-3 cursor-pointer transition"
          :class="form.paymentMethod === 'Pagar en local' ? 'border-brand-red bg-brand-red/5' : 'border-brand-border bg-brand-card'"
        >
          <input v-model="form.paymentMethod" type="radio" value="Pagar en local" class="accent-brand-red" />
          <span>Pagar en local</span>
        </label>
        <label
          class="flex items-center gap-3 justify-between rounded-xl border px-4 py-3 cursor-pointer transition"
          :class="form.paymentMethod === 'Pagar online (demo)' ? 'border-brand-red bg-brand-red/5' : 'border-brand-border bg-brand-card'"
        >
          <span class="flex items-center gap-3">
            <input v-model="form.paymentMethod" type="radio" value="Pagar online (demo)" class="accent-brand-red" />
            <span>Pagar online</span>
          </span>
          <span class="text-xs font-semibold text-brand-text-soft bg-brand-beige rounded-full px-2 py-1">
            Demo / próximamente
          </span>
        </label>
      </div>
      <p v-if="errors.paymentMethod" class="text-brand-red text-sm mt-1">{{ errors.paymentMethod }}</p>
    </div>

    <div>
      <label class="block text-sm font-semibold text-brand-text mb-1" for="note">Nota para cocina (opcional)</label>
      <textarea
        id="note"
        v-model="form.note"
        rows="3"
        placeholder="Ej: sin cebolla, cortar en cuadrados..."
        class="w-full rounded-xl border border-brand-border bg-brand-card px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-red resize-none"
      />
    </div>

    <BaseButton type="submit" class="w-full">Confirmar pedido</BaseButton>
  </form>
</template>
