// IB-Link docs 共通ユーティリティ
// - 現状は Back to top ボタンの挙動のみを提供
(function(){
  /**
   * Back to top ボタンを初期化する
   * @param {string} buttonId - 対象ボタン要素の id
   * @param {number} [threshold=600] - ボタンを表示し始めるスクロール量(px)
   */
  function initBackToTop(buttonId, threshold){
    var btn = document.getElementById(buttonId);
    if(!btn) return;

    var limit = typeof threshold === 'number' ? threshold : 600;

    btn.addEventListener('click', function(){
      window.scrollTo({top:0, behavior:'smooth'});
    });

    window.addEventListener('scroll', function(){
      if(window.scrollY > limit){
        btn.classList.add('show');
      }else{
        btn.classList.remove('show');
      }
    });
  }

  // グローバル名前空間に公開
  window.IBLinkCommon = window.IBLinkCommon || {};
  window.IBLinkCommon.initBackToTop = initBackToTop;
})();


