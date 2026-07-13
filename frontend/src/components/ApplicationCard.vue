<template>
    <div class="card shadow-sm mb-3">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start gap-3">
                <div>
                    <h5>
                        {{ application.title || application.drive_title }}
                    </h5>
                    <p>
                        {{ application.company_name }}
                    </p>
                    <p v-if="application.student_name" class="mb-1 small">
                        <strong>Student:</strong>
                        {{ application.student_name }}
                        <span v-if="application.roll_number">({{ application.roll_number }})</span>
                    </p>
                    <p v-if="application.branch || application.cgpa" class="mb-0 small text-muted">
                        <span v-if="application.branch">{{ application.branch }}</span>
                        <span v-if="application.branch && application.cgpa"> · </span>
                        <span v-if="application.cgpa">CGPA {{ application.cgpa }}</span>
                    </p>
                </div>
                <StatusBadge :status="application.status" />
            </div>
            <div v-if="application.applied_at" class="mt-2 small text-muted">
                Applied: {{ formatDate(application.applied_at) }}
            </div>
            <div v-if="application.status !== 'rejected' && application.interview_date" class="mt-2">
                <strong>Interview:</strong>
                {{ formatDate(application.interview_date) }}
            </div>
            <div v-if="application.remarks" class="mt-2">
                <strong>Remarks:</strong>
                {{ application.remarks }}
            </div>
        </div>
    </div>

</template>

<script>
import StatusBadge from "./StatusBadge.vue"

export default {

    components: {
        StatusBadge
    },
    props: ["application"],
    methods: {

        formatDate(dateString) {
            if (!dateString) return ""
            const date = new Date(dateString)
            return date.toLocaleDateString() + " " + date.toLocaleTimeString()
        }
    }
}

</script>
