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
        isActive: false,
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
        }
    },
})


// jQueryのコード(Vueに置換予定)
$(function() {

    // 食品ページで、ごみ箱ボタンを押すとモーダルを表示する
    $('#food-trash').click(function() {
        $('#trash-confirm-modal').fadeIn();
    });

    // 食品ページで、ごみ箱への移動をキャンセルするとモーダルを非表示にする
    $('#trash-cancel').click(function() {
        $('#trash-confirm-modal').fadeOut();
    });

    // ごみ箱ページで、1つ以上食品にチェックを付けると、完全に削除/元に戻すボタンを活性化する
    $('.trash-check').click(function() {
        $("#food-delete-btn").prop('disabled', false);
        $("#food-restore-btn").prop('disabled', false);
    });

});