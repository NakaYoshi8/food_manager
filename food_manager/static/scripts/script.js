// ダッシュボード
new Vue({
    el: '#dashboard-category',
    data: {
        isActive: false,
        btnText: '+',
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
            if (this.btnText==='+') {
                this.btnText = '-';
            } else {
                this.btnText = '+';
            }
        }
    },
})

new Vue({
    el: '#dashboard-tag',
    data: {
        isActive: false,
        btnText: '+',
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
            if (this.btnText==='+') {
                this.btnText = '-';
            } else {
                this.btnText = '+';
            }
        }
    },
})

new Vue({
    el: '#dashboard-food',
    data: {
        isActive: false,
        btnText: '+',
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
            if (this.btnText==='+') {
                this.btnText = '-';
            } else {
                this.btnText = '+';
            }
        }
    },
})

// 各カテゴリページ
new Vue({
    el: '#category-heading',
    data: {
        isActive: false,
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
        }
    },
})

// 各タグページ
new Vue({
    el: '#tag-heading',
    data: {
        isActive: false,
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
        }
    },
})

// 各食品ページ
new Vue({
    el: '#food-heading',
    data: {
        editFormIsActive: false,
        trashModalIsActive: false,
    },
    methods: {
        changeShowEditForm() {
            this.editFormIsActive = !this.editFormIsActive;
        },
        openTrashModal() {
            this.trashModalIsActive = true;
        },
        closeTrashModal() {
            this.trashModalIsActive = false;
        },
    },
})


// jQueryのコード(Vueに置換予定)
$(function() {

    // ごみ箱ページで、1つ以上食品にチェックを付けると、完全に削除/元に戻すボタンを活性化する
    $('.trash-check').click(function() {
        $("#food-delete-btn").prop('disabled', false);
        $("#food-restore-btn").prop('disabled', false);
    });

});