<template>

<div class="card shadow-sm mb-3">
    <div class="card-body">
        <h5>
            {{ drive.title }}
        </h5>

        <p class="mb-1">
            {{ drive.company_name }}
        </p>

        <p class="text-muted">
            {{ drive.location }}
        </p>

        <p>
            ₹ {{ drive.salary_package }} LPA
        </p>

        <p v-if="drive.application_deadline" class="mb-2 text-danger">
            <strong>Deadline:</strong>
            {{ formatDate(drive.application_deadline) }}
        </p>

        <div v-if="drive.approval_status || drive.status" class="d-flex flex-wrap gap-2 mb-3">
            <StatusBadge v-if="drive.approval_status" :status="drive.approval_status" />
            <StatusBadge v-if="drive.status" :status="drive.status" />
            <span v-if="availabilityLabel" class="badge status-badge" :class="availabilityClass">
                {{ availabilityLabel }}
            </span>
        </div>

        <p v-if="drive.eligible === false && drive.eligibility_message" class="text-warning small mb-3">
            {{ drive.eligibility_message }}
        </p>

        <button
            v-if="showActions"
            class="btn btn-primary"
            @click="$emit('view',drive.id)"
        >
            View Details
        </button>

    </div>

</div>

</template>

<script>

import StatusBadge from "@/components/StatusBadge.vue"

export default{

    components:{
        StatusBadge
    },

    props:{
        drive:{
            type:Object,
            required:true
        },
        showActions:{
            type:Boolean,
            default:true
        }
    },

    computed:{
        availabilityLabel(){
            if(this.drive.status === "closed") return "Closed"
            if(this.isDeadlinePassed) return "Deadline passed"
            if(this.drive.can_apply === true) return "Can apply"
            if(this.drive.can_apply === false) return "Not eligible"
            if(this.drive.eligible === false) return "Not eligible"
            if(this.drive.eligible === true) return "Can apply"
            return ""
        },

        availabilityClass(){
            if(this.availabilityLabel === "Can apply") return "bg-success"
            if(this.availabilityLabel === "Closed") return "bg-secondary"
            if(this.availabilityLabel === "Deadline passed") return "bg-danger"
            return "bg-warning"
        },

        isDeadlinePassed(){
            if(this.drive.deadline_passed === true) return true
            if(!this.drive.application_deadline) return false

            const deadline = this.parseDateOnly(this.drive.application_deadline)
            const today = new Date()
            today.setHours(0, 0, 0, 0)

            return deadline && deadline < today
        }
    },

    methods:{
        formatDate(value){
            if(!value) return ""
            const date = this.parseDateOnly(value) || new Date(value)
            if(Number.isNaN(date.getTime())) return value
            return date.toLocaleDateString()
        },

        parseDateOnly(value){
            const match = String(value).match(/^(\d{4})-(\d{2})-(\d{2})/)
            if(!match) return null

            return new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]))
        }
    }

}

</script>
