<template>
    <div>
        <div class="modal-backdrop fade show"></div>

        <div class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ title || "Confirm" }}</h5>
                        <button
                            type="button"
                            class="btn-close"
                            aria-label="Close"
                            @click="$emit('cancel')"
                        ></button>
                    </div>

                    <div class="modal-body">
                        {{ message }}
                    </div>

                    <div class="modal-footer">
                        <button class="btn btn-secondary" @click="$emit('cancel')">
                            {{ cancelText || "Cancel" }}
                        </button>
                        <button class="btn btn-danger" @click="$emit('confirm')">
                            {{ confirmText || "Confirm" }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ["title", "message", "confirmText", "cancelText"]
}
</script>
