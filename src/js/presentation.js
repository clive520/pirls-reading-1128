const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentSlide = 1;
    let currentStep = 1;

    const pageIndicator = document.getElementById('page-num');
    const progressBar = document.getElementById('progress-bar');
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const btnFullscreen = document.getElementById('btn-fullscreen');
    const btnAgenda = document.getElementById('btn-agenda');
    const agendaModal = document.getElementById('agenda-modal');
    const btnCloseModal = document.getElementById('btn-close-modal');
    const jumpItems = document.querySelectorAll('.jump-item');

    function getSlideStepItems(slideEl) {
      if (!slideEl) return [];
      return Array.from(slideEl.querySelectorAll('.step-item'));
    }

    function applySlideSteps(slideEl, activeStepIndex) {
      const items = getSlideStepItems(slideEl);
      if (items.length === 0) return;

      currentStep = Math.max(1, Math.min(activeStepIndex, items.length));

      items.forEach((item, idx) => {
        const itemStep = idx + 1;
        if (itemStep < currentStep) {
          // 上一點已講過：保留顯示但縮小、輕柔對比
          item.classList.add('revealed');
          item.classList.remove('active-step');
        } else if (itemStep === currentStep) {
          // 正在講的那一點：跳出放大、光暈聚焦！
          item.classList.add('revealed', 'active-step');
        } else {
          // 尚未輪到的點：隱藏
          item.classList.remove('revealed', 'active-step');
        }
      });

      pageIndicator.textContent = `${currentSlide} / ${totalSlides} • 重點 ${currentStep}/${items.length}`;
      btnPrev.disabled = (currentSlide === 1 && currentStep <= 1);
      btnNext.disabled = (currentSlide === totalSlides && currentStep >= items.length);
    }

    function updateSlide(targetIndex, initialStep = 1) {
      if (targetIndex < 1) targetIndex = 1;
      if (targetIndex > totalSlides) targetIndex = totalSlides;

      slides.forEach((slide, idx) => {
        const slideIndex = idx + 1;
        slide.classList.remove('active', 'prev');
        if (slideIndex === targetIndex) {
          slide.classList.add('active');
        } else if (slideIndex < targetIndex) {
          slide.classList.add('prev');
        }
      });

      currentSlide = targetIndex;
      const activeSlideEl = slides[currentSlide - 1];
      const items = getSlideStepItems(activeSlideEl);

      progressBar.style.width = `${(currentSlide / totalSlides) * 100}%`;

      if (items.length > 0) {
        applySlideSteps(activeSlideEl, initialStep);
      } else {
        currentStep = 1;
        pageIndicator.textContent = `${currentSlide} / ${totalSlides}`;
        btnPrev.disabled = (currentSlide === 1);
        btnNext.disabled = (currentSlide === totalSlides);
      }
    }

    function goNext() {
      const activeSlideEl = slides[currentSlide - 1];
      const items = getSlideStepItems(activeSlideEl);

      if (items.length > 0 && currentStep < items.length) {
        // 在當前頁面推進到下一個重點
        applySlideSteps(activeSlideEl, currentStep + 1);
      } else {
        // 當前頁面的重點已全部講完，推進到下一頁
        if (currentSlide < totalSlides) {
          updateSlide(currentSlide + 1, 1);
        }
      }
    }

    function goPrev() {
      const activeSlideEl = slides[currentSlide - 1];
      const items = getSlideStepItems(activeSlideEl);

      if (items.length > 0 && currentStep > 1) {
        // 在當前頁面返回上一個重點
        applySlideSteps(activeSlideEl, currentStep - 1);
      } else {
        // 返回上一頁（若上一頁有重點，直接進入上一頁的最後一個重點）
        if (currentSlide > 1) {
          const prevSlideEl = slides[currentSlide - 2];
          const prevItems = getSlideStepItems(prevSlideEl);
          updateSlide(currentSlide - 1, prevItems.length > 0 ? prevItems.length : 1);
        }
      }
    }

    btnPrev.addEventListener('click', goPrev);
    btnNext.addEventListener('click', goNext);

    // 點擊任何重點卡片，可直接切換聚焦該重點
    document.querySelectorAll('.step-item').forEach(item => {
      item.addEventListener('click', () => {
        const slideEl = item.closest('.slide');
        if (!slideEl || !slideEl.classList.contains('active')) return;
        const items = getSlideStepItems(slideEl);
        const clickedIndex = items.indexOf(item);
        if (clickedIndex !== -1) {
          applySlideSteps(slideEl, clickedIndex + 1);
        }
      });
    });

    window.addEventListener('keydown', (e) => {
      if (agendaModal.classList.contains('active')) {
        if (e.key === 'Escape') agendaModal.classList.remove('active');
        return;
      }
      switch (e.key) {
        case 'ArrowRight':
        case 'PageDown':
        case ' ':
          e.preventDefault();
          goNext();
          break;
        case 'ArrowLeft':
        case 'PageUp':
          e.preventDefault();
          goPrev();
          break;
        case 'Home':
          updateSlide(1, 1);
          break;
        case 'End':
          updateSlide(totalSlides, 1);
          break;
        case 'f':
        case 'F':
          toggleFullscreen();
          break;
        case 'm':
        case 'M':
          agendaModal.classList.toggle('active');
          break;
      }
    });

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => console.warn(err));
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }

    btnFullscreen.addEventListener('click', toggleFullscreen);

    btnAgenda.addEventListener('click', () => agendaModal.classList.add('active'));
    btnCloseModal.addEventListener('click', () => agendaModal.classList.remove('active'));
    agendaModal.addEventListener('click', (e) => {
      if (e.target === agendaModal) agendaModal.classList.remove('active');
    });

    jumpItems.forEach(item => {
      item.addEventListener('click', () => {
        const target = parseInt(item.getAttribute('data-jump'), 10);
        updateSlide(target, 1);
        agendaModal.classList.remove('active');
      });
    });

    let touchStartX = 0;
    let touchEndX = 0;
    window.addEventListener('touchstart', e => { touchStartX = e.changedTouches[0].screenX; }, false);
    window.addEventListener('touchend', e => {
      touchEndX = e.changedTouches[0].screenX;
      if (touchEndX < touchStartX - 50) goNext();
      if (touchEndX > touchStartX + 50) goPrev();
    }, false);

    updateSlide(1, 1);
