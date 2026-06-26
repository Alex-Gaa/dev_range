<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto space-y-6">

      <!-- HEADER -->
      <div class="bg-white border rounded-2xl p-8">
        <h1 class="text-3xl font-bold">Тарифы и оплата</h1>
        <p class="text-slate-500 mt-2">
          Управление подпиской и платежами
        </p>
      </div>

      <!-- CURRENT SUB -->
      <div
        v-if="billingStore.subscription"
        class="bg-white border rounded-2xl p-8 space-y-3"
      >
        <h2 class="text-xl font-semibold mb-2">
          Текущая подписка
        </h2>

        <div class="flex justify-between">
          <span>Тариф</span>
          <span class="font-medium">
            {{ billingStore.subscription.plan_name || billingStore.subscription.plan }}
          </span>
        </div>

        <div class="flex justify-between">
          <span>Статус</span>
          <span class="font-medium">
            {{ billingStore.subscription.status }}
          </span>
        </div>

        <div class="flex justify-between">
          <span>Использовано уроков</span>
          <span>
            {{ formatPlural(
              billingStore.subscription.lessons_used,
              'урок использован',
              'урока использовано',
              'уроков использовано'
            ) }}
          </span>
        </div>

        <div class="flex justify-between">
          <span>Действует до</span>
          <span>{{ formatDate(billingStore.subscription.expires_at) }}</span>
        </div>

        <!-- UPGRADE (FIXED) -->
        <button
          v-if="featuredPlan"
          @click="openCheckout(featuredPlan)"
          class="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-xl"
        >
          Улучшить тариф
        </button>
      </div>

      <!-- PLANS -->
      <div class="grid md:grid-cols-3 gap-4">

        <div
          v-for="plan in plans"
          :key="plan.id"
          class="bg-white border rounded-2xl p-6 space-y-3"
        >
          <h3 class="text-xl font-semibold">
            {{ plan.title }}
          </h3>

          <div class="text-2xl font-bold">
            {{ plan.price }} ₽
          </div>

          <ul class="text-sm text-slate-600 space-y-1">
            <li>
              ✔ {{ formatPlural(plan.lessons, 'урок', 'урока', 'уроков') }}
            </li>
            <li>
              ✔ {{ formatPlural(plan.children, 'ученик', 'ученика', 'учеников') }}
            </li>
            <li>✔ AI доступ</li>
          </ul>

          <button
            @click="openCheckout(plan)"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-xl"
          >
            Выбрать тариф
          </button>
        </div>

      </div>

      <!-- MODAL -->
      <div
        v-if="checkoutPlan"
        class="fixed inset-0 bg-black/50 flex items-center justify-center"
      >
        <div class="bg-white rounded-2xl p-6 w-[420px] space-y-4">

          <h2 class="text-xl font-bold">
            Подтверждение оплаты
          </h2>

          <p>
            Вы выбрали тариф:
            <b>{{ checkoutPlan.title }}</b>
          </p>

          <div class="bg-slate-50 p-3 rounded-lg text-sm">
            Тестовая оплата. Деньги не списываются.
          </div>

          <div class="flex gap-2 justify-end">

            <button
              @click="checkoutPlan = null"
              class="px-4 py-2 rounded-lg border"
            >
              Отмена
            </button>

            <button
              @click="pay"
              class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
            >
              Оплатить
            </button>

          </div>

        </div>
      </div>

    </div>
  </AppLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import { useBillingStore } from "@/stores/billing"
import api from "@/api/axios"

const billingStore = useBillingStore()

const plans = ref([])
const checkoutPlan = ref(null)
const featuredCode = ref(null)

/* LOAD */
onMounted(async () => {
  await billingStore.fetchSubscription()

  const res = await api.get("/billing/plans/")

  // FIX: берем featured с backend
  featuredCode.value = res.data.featured

  plans.value = (res.data.plans || []).map(p => ({
    id: p.code,
    title: p.name,
    price: p.price,
    lessons: p.lessons_limit,
    children: p.children_limit
  }))
})

/* FEATURED PLAN (FIXED) */
const featuredPlan = computed(() => {
  return plans.value.find(p => p.id === featuredCode.value)
})

/* CHECKOUT */
const openCheckout = (plan) => {
  checkoutPlan.value = plan
}

/* PAY */
const pay = async () => {
  const planId = checkoutPlan.value?.id
  checkoutPlan.value = null

  await new Promise(r => setTimeout(r, 800))

  await billingStore.activate(planId)
  await billingStore.fetchSubscription()
}

/* UTILS */
const formatPlural = (count, one, few, many) => {
  if (count % 100 >= 11 && count % 100 <= 14) {
    return `${count} ${many}`
  }

  switch (count % 10) {
    case 1:
      return `${count} ${one}`
    case 2:
    case 3:
    case 4:
      return `${count} ${few}`
    default:
      return `${count} ${many}`
  }
}

const formatDate = (date) => {
  if (!date) return ""
  return new Date(date).toLocaleDateString("ru-RU")
}
</script>