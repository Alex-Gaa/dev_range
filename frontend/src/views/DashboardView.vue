<template>

  <AppLayout>

    <div class="grid grid-cols-3 gap-6">

      <BaseCard>

        <h3 class="text-lg font-semibold">
          Children
        </h3>

        <p class="text-3xl mt-4 font-bold">
          2
        </p>

      </BaseCard>

      <BaseCard>

        <h3 class="text-lg font-semibold">
          Lessons completed
        </h3>

        <p class="text-3xl mt-4 font-bold">
          48
        </p>

      </BaseCard>

      <BaseCard>

        <h3 class="text-lg font-semibold">
          AI Tokens
        </h3>

        <p class="text-3xl mt-4 font-bold">
          1200
        </p>

      </BaseCard>

    </div>

  </AppLayout>

</template>

<script setup>
import AppLayout from "@/layouts/AppLayout.vue"
import BaseCard from "@/components/ui/BaseCard.vue"
</script>