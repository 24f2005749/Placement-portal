<template>
    <div class="card mb-3">
        <div class="card-body">
            <h5>
                {{ student.full_name }}
            </h5>
            <p>
                {{ student.branch }}
            </p>
            <p>
                CGPA {{ student.cgpa }}
            </p>
            <button v-if="showActions" class="btn btn-outline-primary" @click="$emit('view', student.id)">
                View
            </button>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        student: {
            type: Object,
            required: true
        },
        showActions: {
            type: Boolean,
            default: true
        }
    }
}
</script>
